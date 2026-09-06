"""Migration recovery contracts; the double does not claim to execute DSQL SQL."""

from dataclasses import dataclass
from typing import cast
from unittest.mock import patch

import pytest
from psycopg import Connection

pytest.importorskip("sqlglot", reason="migration plans require the locked SQL parser")

from database.migrate import (
    Migration,
    PreparedMigration,
    apply_migrations,
    load_migrations,
    main,
)

DDL = "CREATE TABLE recipeweave.contract_fixture (id TEXT PRIMARY KEY)"
VERIFY = "SELECT TRUE"


class InterruptedLedgerWrite(Exception):
    """A committed DDL can survive interruption before its ledger DML."""


@dataclass
class Result:
    row: tuple[object, ...] | None = None

    def fetchone(self) -> tuple[object, ...] | None:
        return self.row


@dataclass
class MigrationBoundary:
    """Only the externally observable schema/ledger states, not a database emulator."""

    schema_ready: bool = False
    ledger_checksum: str | None = None
    ddl_passes_postcondition: bool = True
    interrupt_before_ledger: bool = False
    ddl_writes: int = 0
    ledger_writes: int = 0

    def execute(self, statement: str | bytes, params: tuple[str, ...] = ()) -> Result:
        text = statement.decode("utf-8") if isinstance(statement, bytes) else statement
        if text.startswith("CREATE SCHEMA IF NOT EXISTS") or text.startswith(
            "CREATE TABLE IF NOT EXISTS recipeweave.schema_migrations"
        ):
            return Result()
        if text.startswith("SELECT checksum FROM recipeweave.schema_migrations"):
            return Result(None if self.ledger_checksum is None else (self.ledger_checksum,))
        if text == VERIFY:
            return Result((self.schema_ready,))
        if text == DDL:
            self.ddl_writes += 1
            self.schema_ready = self.ddl_passes_postcondition
            return Result()
        if text.startswith("INSERT INTO recipeweave.schema_migrations"):
            if self.interrupt_before_ledger:
                self.interrupt_before_ledger = False
                raise InterruptedLedgerWrite()
            self.ledger_checksum = params[1]
            self.ledger_writes += 1
            return Result()
        raise AssertionError("Unexpected operation outside migration recovery contract")

    def connection(self) -> Connection[tuple[object, ...]]:
        return cast(Connection[tuple[object, ...]], self)


@pytest.fixture
def migration() -> PreparedMigration:
    definition = Migration(id="contract-fixture", file="fixture.sql", kind="ddl", verify=VERIFY)
    return PreparedMigration(definition, DDL, "a" * 64)


def test_plan_is_repeatable_and_never_connects_to_aws(capsys: pytest.CaptureFixture[str]) -> None:
    with (
        patch("sys.argv", ["migrate.py", "--plan"]),
        patch("database.migrate.connect_admin") as connection,
    ):
        assert main() == 0
        first = capsys.readouterr().out
        assert main() == 0
        assert capsys.readouterr().out == first
        assert "001_user_state" in first
        assert len(load_migrations()[0].checksum) == 64
        connection.assert_not_called()


def test_ledger_match_is_idempotent_and_mismatch_stops(migration: PreparedMigration) -> None:
    boundary = MigrationBoundary(schema_ready=True, ledger_checksum=migration.checksum)
    apply_migrations(boundary.connection(), [migration])
    assert boundary.ddl_writes == boundary.ledger_writes == 0
    boundary.ledger_checksum = "b" * 64
    with pytest.raises(ValueError, match="checksum mismatch"):
        apply_migrations(boundary.connection(), [migration])
    assert boundary.ddl_writes == boundary.ledger_writes == 0
    assert boundary.ledger_checksum == "b" * 64


def test_resume_after_committed_ddl_does_not_repeat_ddl(migration: PreparedMigration) -> None:
    boundary = MigrationBoundary(interrupt_before_ledger=True)
    with pytest.raises(InterruptedLedgerWrite):
        apply_migrations(boundary.connection(), [migration])
    assert boundary.schema_ready
    assert boundary.ddl_writes == 1
    assert boundary.ledger_checksum is None
    apply_migrations(boundary.connection(), [migration])
    assert boundary.ddl_writes == 1
    assert boundary.ledger_writes == 1
    assert boundary.ledger_checksum == migration.checksum


def test_failed_postcondition_never_records_success(migration: PreparedMigration) -> None:
    boundary = MigrationBoundary(ddl_passes_postcondition=False)
    with pytest.raises(ValueError, match="postcondition failed"):
        apply_migrations(boundary.connection(), [migration])
    assert boundary.ddl_writes == 1
    assert boundary.ledger_checksum is None
    assert boundary.ledger_writes == 0
