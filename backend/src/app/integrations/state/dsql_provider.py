"""Aurora DSQL adapter: verified TLS, IAM on each connection and bounded OCC retry."""

import re
import time
from collections.abc import Callable
from typing import Protocol, TypeVar, cast

import boto3
import certifi
import psycopg
from botocore.config import Config
from psycopg import Connection
from psycopg.errors import SerializationFailure, UniqueViolation
from pydantic import JsonValue

from app.apis.state.get_state.generated.queries import select_state
from app.apis.state.put_state.generated.queries import insert_state, update_state
from app.core.errors import ServiceUnavailableError, StateConflictError
from app.core.models import AppSnapshot, StateEnvelope
from app.core.settings import AppSettings


class DsqlTokenClient(Protocol):
    """Boto3 custom presigning methods omitted by its generated service stubs."""

    def generate_db_connect_auth_token(
        self, *, Hostname: str, Region: str, ExpiresIn: int
    ) -> str: ...


T = TypeVar("T")


class DsqlStateRepository:
    def __init__(self, settings: AppSettings) -> None:
        if not re.fullmatch(r"[a-z0-9]+\.dsql\.[a-z0-9-]+\.on\.aws", settings.dsql_host):
            raise ServiceUnavailableError("DSQL endpoint missing or invalid")
        if not re.fullmatch(r"[a-z][a-z0-9_]{0,62}", settings.dsql_database_user):
            raise ServiceUnavailableError("DSQL application role invalid")
        if settings.dsql_database_user == "admin":
            raise ServiceUnavailableError("admin role is forbidden for application requests")
        self._settings = settings
        # Dynamic SDK method boundary is narrowed here; operation code sees only StateRepository.
        client_factory: Callable[..., DsqlTokenClient] = getattr(boto3, "client")  # noqa: B009 -- dynamic SDK typing boundary
        self._client = client_factory(
            "dsql",
            region_name=settings.aws_region,
            config=Config(
                retries={"total_max_attempts": 3, "mode": "standard"},
                connect_timeout=5,
                read_timeout=10,
            ),
        )

    def _connect(self) -> Connection[tuple[object, ...]]:
        token = self._client.generate_db_connect_auth_token(
            Hostname=self._settings.dsql_host,
            Region=self._settings.aws_region,
            ExpiresIn=900,
        )
        return cast(
            Connection[tuple[object, ...]],
            psycopg.connect(
                host=self._settings.dsql_host,
                port=5432,
                dbname="postgres",
                user=self._settings.dsql_database_user,
                password=token,
                sslmode="verify-full",
                sslrootcert=certifi.where(),
                connect_timeout=5,
            ),
        )

    def _transaction(self, operation: Callable[[Connection[tuple[object, ...]]], T]) -> T:
        for attempt in range(3):
            try:
                with self._connect() as connection:
                    return operation(connection)
            except UniqueViolation as exc:
                raise StateConflictError("state version conflict") from exc
            except SerializationFailure as exc:
                if attempt == 2:
                    raise ServiceUnavailableError(
                        "concurrent database transactions; retry later"
                    ) from exc
                time.sleep(0.02 * (2**attempt))
            except psycopg.OperationalError as exc:
                raise ServiceUnavailableError("database unavailable") from exc
        raise ServiceUnavailableError("transaction attempts exhausted")

    def get(self, subject: str) -> StateEnvelope:
        def read(connection: Connection[tuple[object, ...]]) -> StateEnvelope:
            row = select_state(connection, subject)
            if row is None:
                return StateEnvelope(version=0, snapshot=None)
            return StateEnvelope(
                version=row.revision, snapshot=AppSnapshot.model_validate(row.payload)
            )

        return self._transaction(read)

    def put(self, subject: str, expected_version: int, snapshot: AppSnapshot) -> StateEnvelope:
        payload = cast(dict[str, JsonValue], snapshot.model_dump(mode="json", by_alias=True))

        def write(connection: Connection[tuple[object, ...]]) -> StateEnvelope:
            if expected_version == 0:
                insert_state(connection, subject, payload)
            elif not update_state(connection, subject, expected_version, payload):
                raise StateConflictError("state version conflict")
            return StateEnvelope(version=expected_version + 1, snapshot=snapshot)

        return self._transaction(write)
