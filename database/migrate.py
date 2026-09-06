"""One DDL per transaction, checksummed ledger and separate DML transactions.

Use --plan without AWS. --apply requires an already-assumed dedicated migration
IAM role with DbConnectAdmin. Runtime Lambda has only DbConnect.
"""

import argparse
import hashlib
import json
import os
import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, LiteralString, Protocol, cast

import boto3
import certifi
import psycopg
import sqlglot
from botocore.config import Config
from psycopg import Connection, sql
from pydantic import BaseModel, ConfigDict

ROOT = Path(__file__).resolve().parent


class AdminTokenClient(Protocol):
    def generate_db_connect_admin_auth_token(
        self, *, Hostname: str, Region: str, ExpiresIn: int
    ) -> str: ...


class Migration(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    id: str
    file: str
    kind: Literal["ddl", "dml", "index"]
    verify: str


class Manifest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    schemaVersion: Literal[1]
    migrations: list[Migration]


@dataclass(frozen=True)
class PreparedMigration:
    definition: Migration
    statement: str
    checksum: str


def load_migrations(path: Path = ROOT / "migrations") -> list[PreparedMigration]:
    """Validate declarations before any database action."""
    manifest = Manifest.model_validate_json((path / "manifest.manual.json").read_text())
    result: list[PreparedMigration] = []
    seen: set[str] = set()
    for item in manifest.migrations:
        source = path / item.file
        if source.parent != path or source.is_symlink() or item.id in seen:
            raise ValueError("invalid migration path or duplicate identity")
        seen.add(item.id)
        statement = source.read_text()
        parsed = statement.replace("INDEX ASYNC", "INDEX", 1) if item.kind == "index" else statement
        if len(sqlglot.parse(parsed, read="postgres")) != 1:
            raise ValueError("each migration must contain one SQL statement")
        if len(sqlglot.parse(item.verify, read="postgres")) != 1:
            raise ValueError("each verification must contain one SQL query")
        checksum = hashlib.sha256((statement + "\n" + item.verify).encode()).hexdigest()
        result.append(PreparedMigration(item, statement, checksum))
    return result


def connect_admin(host: str, region: str) -> Connection[tuple[object, ...]]:
    if not re.fullmatch(r"[a-z0-9]+\.dsql\.[a-z0-9-]+\.on\.aws", host):
        raise ValueError("invalid DSQL_HOST")
    factory: Callable[..., AdminTokenClient] = getattr(boto3, "client")  # noqa: B009 -- dynamic SDK typing boundary
    client = factory(
        "dsql",
        region_name=region,
        config=Config(
            retries={"total_max_attempts": 3, "mode": "standard"},
            connect_timeout=5,
            read_timeout=10,
        ),
    )
    token = client.generate_db_connect_admin_auth_token(Hostname=host, Region=region, ExpiresIn=900)
    return cast(
        Connection[tuple[object, ...]],
        psycopg.connect(
            host=host,
            port=5432,
            dbname="postgres",
            user="admin",
            password=token,
            sslmode="verify-full",
            sslrootcert=certifi.where(),
            connect_timeout=5,
            autocommit=True,
        ),
    )


def verified(connection: Connection[tuple[object, ...]], statement: str) -> bool:
    row = connection.execute(sql.SQL(cast(LiteralString, statement))).fetchone()
    return row is not None and row[0] is True


def apply_migrations(
    connection: Connection[tuple[object, ...]], items: list[PreparedMigration]
) -> None:
    """Recover a committed DDL before ledger write only after structural verification."""
    connection.execute("CREATE SCHEMA IF NOT EXISTS recipeweave")
    connection.execute(
        "CREATE TABLE IF NOT EXISTS recipeweave.schema_migrations "
        "(id TEXT PRIMARY KEY, checksum TEXT NOT NULL, applied_at TIMESTAMPTZ NOT NULL)"
    )
    for item in items:
        definition = item.definition
        row = connection.execute(
            "SELECT checksum FROM recipeweave.schema_migrations WHERE id = %s", (definition.id,)
        ).fetchone()
        if row is not None:
            if row[0] != item.checksum:
                raise ValueError(f"migration checksum mismatch: {definition.id}")
            if not verified(connection, definition.verify):
                raise ValueError(f"applied schema drift: {definition.id}")
            continue
        if not verified(connection, definition.verify):
            cursor = connection.execute(sql.SQL(cast(LiteralString, item.statement)))
            if definition.kind == "index":
                job = cursor.fetchone()
                if job is None or not isinstance(job[0], str):
                    raise ValueError("async index creation returned no job id")
                result = connection.execute("SELECT sys.wait_for_job(%s)", (job[0],)).fetchone()
                if result is None or result[0] is not True:
                    raise ValueError("async index creation failed")
            if not verified(connection, definition.verify):
                raise ValueError(f"migration postcondition failed: {definition.id}")
        # This DML is separate from the preceding DDL autocommit transaction.
        connection.execute(
            "INSERT INTO recipeweave.schema_migrations (id, checksum, applied_at) "
            "VALUES (%s, %s, CURRENT_TIMESTAMP)",
            (definition.id, item.checksum),
        )


def grant_application(connection: Connection[tuple[object, ...]], iam_arn: str) -> None:
    """Bind the non-admin application database role to exactly the supplied IAM role."""
    if not re.fullmatch(r"arn:aws(?:-cn|-us-gov)?:iam::\d{12}:role/[A-Za-z0-9+=,.@_/-]+", iam_arn):
        raise ValueError("invalid DSQL_APP_IAM_ARN")
    row = connection.execute(
        "SELECT rolname FROM pg_roles WHERE rolname = %s", ("recipeweave_app",)
    ).fetchone()
    if row is None:
        connection.execute("CREATE ROLE recipeweave_app WITH LOGIN")
    connection.execute(sql.SQL("AWS IAM GRANT recipeweave_app TO {}").format(sql.Literal(iam_arn)))
    connection.execute("GRANT USAGE ON SCHEMA recipeweave TO recipeweave_app")
    connection.execute("GRANT SELECT, INSERT, UPDATE ON recipeweave.user_state TO recipeweave_app")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument("--plan", action="store_true")
    choice.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    items = load_migrations()
    if not args.apply:
        print(
            json.dumps(
                [
                    {
                        "id": item.definition.id,
                        "sha256": item.checksum,
                        "kind": item.definition.kind,
                    }
                    for item in items
                ],
                indent=2,
            )
        )
        return 0
    app_arn = os.environ["DSQL_APP_IAM_ARN"]
    with connect_admin(
        os.environ["DSQL_HOST"], os.environ.get("AWS_REGION", "ap-northeast-1")
    ) as connection:
        apply_migrations(connection, items)
        grant_application(connection, app_arn)
    print("Migrations and application grants completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
