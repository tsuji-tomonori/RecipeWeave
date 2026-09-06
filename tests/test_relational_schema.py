"""原設計の網羅性とPostgreSQLで拒否すべき関係・ライフサイクルを検証する。"""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import pglast
import psycopg
import pytest
from psycopg import sql

from database.migrate import apply_migrations, load_migrations
from database.schema_catalog import extract, split_sql

ROOT = Path(__file__).resolve().parents[1]


def test_all_source_columns_and_foreign_keys_are_implemented() -> None:
    source = json.loads((ROOT / "spec/database/source-sheet.json").read_text())["tabs"]
    catalog = extract(ROOT)
    tables = {table["name"]: table for table in catalog["tables"]}
    original_tables = {row[2] for row in source["01_テーブル一覧"][1:]}
    assert len(original_tables) == 71
    assert original_tables <= tables.keys()
    assert len(source["02_カラム辞書"][1:]) == 554
    assert sum(len(tables[t]["columns"]) for t in original_tables) >= 554
    for table, _, name, datatype, nullable, *_ in source["02_カラム辞書"][1:]:
        actual = next(c for c in tables[table]["columns"] if c["name"] == name)
        assert actual["type"] == datatype
        if f"{table}.{name}" not in catalog["column_evolutions"]:
            assert actual["nullable"] == (nullable == "可")
    for table, _, name, _, _, rule, *_ in source["02_カラム辞書"][1:]:
        if rule.startswith("CHECK IN ("):
            expected_values = set(rule.removeprefix("CHECK IN (").removesuffix(")").split(","))
            actual = next(c for c in tables[table]["columns"] if c["name"] == name)
            assert expected_values <= set(actual["enum"]), (table, name)
    for child, column, parent, target, _, delete, *_ in source["04_外部キー"][1:]:
        assert any(
            fk["columns"] == [column]
            and fk["referenced_table"] == parent
            and fk["referenced_columns"] == [target]
            and fk["on_delete"] == delete
            and fk["deferrable"]
            for fk in tables[child]["foreign_keys"]
        ), (child, column)


def test_all_migration_statements_parse_as_postgresql() -> None:
    for migration in sorted((ROOT / "database/migrations").glob("*.sql")):
        assert pglast.parse_sql(migration.read_text())


def test_catalog_is_deterministic_and_not_a_spreadsheet_copy() -> None:
    assert extract(ROOT) == extract(ROOT)
    catalog = extract(ROOT)
    unit = next(t for t in catalog["tables"] if t["name"] == "unit")
    assert "CREATE TABLE" in unit["source"]["sql"]
    assert any("factor > 0" == check for check in unit["checks"])
    assert unit["source"]["sha256"]
    assert len(catalog["statements"]) > 1000


def test_sql_split_preserves_function_and_quoted_separators() -> None:
    script = "SELECT 'x;y'; CREATE FUNCTION f() RETURNS text LANGUAGE sql AS $$SELECT 'a;b';$$;"
    assert len(split_sql(script)) == 2
    assert split_sql("a NUMERIC(20,6), CHECK (x IN ('a,b','c'))", ",") == [
        "a NUMERIC(20,6)",
        "CHECK (x IN ('a,b','c'))",
    ]


def test_backup_evidence_is_generated_from_ddl_and_kept_out_of_replacement() -> None:
    tables = {table["name"]: table for table in extract()["tables"]}
    for name in ("backup_artifact", "backup_restore_intent"):
        table = tables[name]
        assert table["retention"] == "audit"
        assert table["owner_path"] == ["user_id"]
        assert table["source"]["file"].endswith("004_backup_restore.sql")
        assert all(column["description"] for column in table["columns"])
        assert not any(column["type"] in {"json", "jsonb"} for column in table["columns"])
        owner = next(fk for fk in table["foreign_keys"] if fk["columns"] == ["user_id"])
        assert owner["referenced_table"] == "app_user"
        assert owner["on_delete"] == "SET NULL"
    names_from_ddl = {
        table["name"]
        for table in tables.values()
        if table["source"]["file"].endswith("004_backup_restore.sql")
    }
    assert names_from_ddl == {"backup_artifact", "backup_restore_intent"}


@pytest.fixture(scope="module")
def migrated_url() -> str:
    value = (
        os.getenv("MIGRATION_DATABASE_URL")
        or os.getenv("TEST_DATABASE_URL")
        or os.getenv("DATABASE_URL")
    )
    if not value and os.getenv("CI"):
        pytest.fail("CIではPostgreSQL結合試験用の接続設定が必須です")
    if not value:
        pytest.skip("PostgreSQL結合試験にはDATABASE_URLが必要です")
    with psycopg.connect(value, autocommit=True) as connection:
        apply_migrations(connection, load_migrations())
    return value


@pytest.fixture
def connection(migrated_url: str) -> Iterator[psycopg.Connection[Any]]:
    with psycopg.connect(migrated_url) as connection:
        connection.execute("SELECT set_config('recipeweave.role', 'admin', true)")
        yield connection
        connection.rollback()


def insert(connection: psycopg.Connection[Any], table: str, **values: Any) -> UUID:
    identity = values.setdefault("id", uuid4())
    connection.execute(
        sql.SQL("INSERT INTO recipeweave.{} ({}) VALUES ({})").format(
            sql.Identifier(table),
            sql.SQL(", ").join(sql.Identifier(key) for key in values),
            sql.SQL(", ").join(sql.Placeholder() for _ in values),
        ),
        list(values.values()),
    )
    return identity


@pytest.fixture
def backup_evidence(connection: psycopg.Connection[Any]) -> dict[str, UUID]:
    user = insert(
        connection,
        "app_user",
        auth_subject=str(uuid4()),
        state="active",
        locale="ja-JP",
        timezone="Asia/Tokyo",
    )
    workspace = insert(connection, "workspace_revision", user_id=user, revision=7)
    artifact = insert(
        connection, "backup_artifact", user_id=user, body_sha256="a" * 64, format_version=2
    )
    intent = insert(
        connection,
        "backup_restore_intent",
        user_id=user,
        artifact_id=artifact,
        body_sha256="a" * 64,
        current_revision=7,
        expires_at=datetime.now(UTC) + timedelta(minutes=10),
    )
    connection.execute("SET CONSTRAINTS ALL IMMEDIATE")
    return dict(user=user, workspace=workspace, artifact=artifact, intent=intent)


@pytest.mark.parametrize("action", ["digest", "created_at", "delete"])
def test_backup_artifact_is_append_only(
    connection: psycopg.Connection[Any], backup_evidence: dict[str, UUID], action: str
) -> None:
    statements = {
        "digest": "UPDATE recipeweave.backup_artifact SET body_sha256=%s WHERE id=%s",
        "created_at": "UPDATE recipeweave.backup_artifact SET created_at=%s WHERE id=%s",
        "delete": "DELETE FROM recipeweave.backup_artifact WHERE id=%s",
    }
    parameters: tuple[object, ...] = (backup_evidence["artifact"],)
    if action == "digest":
        parameters = ("b" * 64, backup_evidence["artifact"])
    elif action == "created_at":
        parameters = (datetime.now(UTC) - timedelta(days=1), backup_evidence["artifact"])
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute(statements[action], parameters)


@pytest.mark.parametrize("fault", ["digest", "owner", "revision", "expired", "consumed"])
def test_backup_intent_rejects_untrusted_or_stale_preview(
    connection: psycopg.Connection[Any], backup_evidence: dict[str, UUID], fault: str
) -> None:
    values: dict[str, Any] = dict(
        user_id=backup_evidence["user"],
        artifact_id=backup_evidence["artifact"],
        body_sha256="a" * 64,
        current_revision=7,
        expires_at=datetime.now(UTC) + timedelta(minutes=10),
    )
    if fault == "digest":
        values["body_sha256"] = "b" * 64
    elif fault == "owner":
        values["user_id"] = insert(
            connection,
            "app_user",
            auth_subject=str(uuid4()),
            state="active",
            locale="ja-JP",
            timezone="Asia/Tokyo",
        )
    elif fault == "revision":
        values["current_revision"] = 6
    elif fault == "expired":
        values["created_at"] = datetime.now(UTC) - timedelta(minutes=10)
        values["expires_at"] = datetime.now(UTC) - timedelta(minutes=1)
    else:
        values["consumed_at"] = datetime.now(UTC)
    with pytest.raises(psycopg.errors.CheckViolation):
        insert(connection, "backup_restore_intent", **values)


def test_backup_intent_is_consumed_once_and_rollback_restores_the_confirmation(
    connection: psycopg.Connection[Any], backup_evidence: dict[str, UUID]
) -> None:
    update = "UPDATE recipeweave.backup_restore_intent SET consumed_at=now() WHERE id=%s"
    connection.execute("SAVEPOINT restore_attempt")
    connection.execute(update, (backup_evidence["intent"],))
    connection.execute("ROLLBACK TO SAVEPOINT restore_attempt")
    row = connection.execute(
        "SELECT consumed_at FROM recipeweave.backup_restore_intent WHERE id=%s",
        (backup_evidence["intent"],),
    ).fetchone()
    assert row is not None and row[0] is None
    connection.execute(update, (backup_evidence["intent"],))
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute(update, (backup_evidence["intent"],))


def test_backup_intent_rejects_changes_after_preview(
    connection: psycopg.Connection[Any], backup_evidence: dict[str, UUID]
) -> None:
    connection.execute(
        "UPDATE recipeweave.workspace_revision SET revision=revision+1 WHERE id=%s",
        (backup_evidence["workspace"],),
    )
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute(
            "UPDATE recipeweave.backup_restore_intent SET consumed_at=now() WHERE id=%s",
            (backup_evidence["intent"],),
        )


@pytest.mark.parametrize("action", ["delete", "extend", "clear"])
def test_backup_intent_cannot_be_deleted_extended_or_reused(
    connection: psycopg.Connection[Any], backup_evidence: dict[str, UUID], action: str
) -> None:
    connection.execute(
        "UPDATE recipeweave.backup_restore_intent SET consumed_at=now() WHERE id=%s",
        (backup_evidence["intent"],),
    )
    statements = {
        "delete": "DELETE FROM recipeweave.backup_restore_intent WHERE id=%s",
        "extend": "UPDATE recipeweave.backup_restore_intent "
        "SET expires_at=expires_at+interval '1 minute' WHERE id=%s",
        "clear": "UPDATE recipeweave.backup_restore_intent SET consumed_at=NULL WHERE id=%s",
    }
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute(statements[action], (backup_evidence["intent"],))


def test_backup_evidence_is_anonymized_when_account_is_erased(
    connection: psycopg.Connection[Any], backup_evidence: dict[str, UUID]
) -> None:
    connection.execute("DELETE FROM recipeweave.app_user WHERE id=%s", (backup_evidence["user"],))
    for table, key in (("backup_artifact", "artifact"), ("backup_restore_intent", "intent")):
        row = connection.execute(
            sql.SQL("SELECT user_id, body_sha256 FROM recipeweave.{} WHERE id=%s").format(
                sql.Identifier(table)
            ),
            (backup_evidence[key],),
        ).fetchone()
        assert row == (None, "a" * 64)


def test_backup_evidence_rls_hides_other_owner_and_rejects_forged_issue(
    connection: psycopg.Connection[Any], backup_evidence: dict[str, UUID]
) -> None:
    other = insert(
        connection,
        "app_user",
        auth_subject=str(uuid4()),
        state="active",
        locale="ja-JP",
        timezone="Asia/Tokyo",
    )
    role = sql.Identifier("recipeweave_backup_test_" + uuid4().hex)
    connection.execute(sql.SQL("CREATE ROLE {} NOLOGIN NOSUPERUSER NOBYPASSRLS").format(role))
    connection.execute(sql.SQL("GRANT USAGE ON SCHEMA recipeweave TO {}").format(role))
    connection.execute(
        sql.SQL(
            "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA recipeweave TO {}"
        ).format(role)
    )
    connection.execute(sql.SQL("SET LOCAL ROLE {}").format(role))
    connection.execute(
        "SELECT set_config('recipeweave.role', 'user', true), "
        "set_config('recipeweave.user_id', %s, true)",
        (str(other),),
    )
    for table in ("backup_artifact", "backup_restore_intent"):
        rows = connection.execute(
            sql.SQL("SELECT id FROM recipeweave.{} WHERE user_id=%s").format(sql.Identifier(table)),
            (backup_evidence["user"],),
        ).fetchall()
        assert rows == []
    with pytest.raises(psycopg.errors.InsufficientPrivilege):
        insert(
            connection,
            "backup_artifact",
            user_id=backup_evidence["user"],
            body_sha256="b" * 64,
            format_version=2,
        )


@pytest.fixture
def task_context(connection: psycopg.Connection[Any], recipe: dict[str, UUID]) -> dict[str, Any]:
    manual_rule = insert(
        connection,
        "scaling_rule",
        name="時間の手動確認",
        mode="manual",
        min_servings=1,
        max_servings=1000,
        round_mode="none",
        round_increment=1,
    )
    connection.execute(
        "UPDATE recipeweave.recipe_step SET scaling_rule_id=%s WHERE id=%s",
        (manual_rule, recipe["step"]),
    )
    user = insert(
        connection,
        "app_user",
        auth_subject=str(uuid4()),
        state="active",
        locale="ja-JP",
        timezone="Asia/Tokyo",
    )
    menu = insert(connection, "menu", user_id=user, name="調理時間試験", servings=2, revision=1)
    item = insert(
        connection,
        "menu_item",
        menu_id=menu,
        recipe_version_id=recipe["version"],
        servings=2,
        position=1,
    )
    session = insert(
        connection,
        "cooking_session",
        menu_id=menu,
        menu_revision=1,
        status="planned",
        planner_version="duration-test",
        input_hash="1" * 64,
        input_snapshot='{"schema_version":1,"menu_revision":1,"items":[],"ingredients":[],"resources":[],"planner_config":{}}',
    )
    return dict(
        session_id=session,
        menu_item_id=item,
        step_id=recipe["step"],
        batch_no=1,
        planned_start_s=0,
        planned_end_s=60,
        status="pending",
    )


@pytest.mark.parametrize(
    ("source", "confirmed", "end"),
    [
        ("user_estimate", None, 60),
        ("user_estimate", 59, 60),
        ("user_estimate", 0, 0),
        ("user_estimate", 86401, 86401),
        ("recipe_rule", 60, 60),
    ],
)
def test_task_duration_requires_consistent_user_confirmation(
    connection: psycopg.Connection[Any],
    task_context: dict[str, Any],
    source: str,
    confirmed: int | None,
    end: int,
) -> None:
    task_context.update(duration_source=source, confirmed_duration_s=confirmed, planned_end_s=end)
    with pytest.raises(psycopg.errors.CheckViolation):
        insert(connection, "session_task", **task_context)


def test_user_time_estimate_is_only_valid_for_manual_steps(
    connection: psycopg.Connection[Any], recipe: dict[str, UUID], task_context: dict[str, Any]
) -> None:
    connection.execute(
        "UPDATE recipeweave.recipe_step SET scaling_rule_id=%s WHERE id=%s",
        (recipe["rule"], recipe["step"]),
    )
    with pytest.raises(psycopg.errors.CheckViolation):
        insert(
            connection,
            "session_task",
            **task_context,
            duration_source="user_estimate",
            confirmed_duration_s=60,
        )


@pytest.mark.parametrize("column", ["step_id", "menu_item_id", "session_id", "batch_no"])
def test_user_confirmed_task_cannot_be_reassigned(
    connection: psycopg.Connection[Any], task_context: dict[str, Any], column: str
) -> None:
    task = insert(
        connection,
        "session_task",
        **task_context,
        duration_source="user_estimate",
        confirmed_duration_s=60,
    )
    value: UUID | int = 2 if column == "batch_no" else uuid4()
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute(
            sql.SQL("UPDATE recipeweave.session_task SET {}=%s WHERE id=%s").format(
                sql.Identifier(column)
            ),
            (value, task),
        )


@pytest.mark.parametrize(
    "column", ["duration_source", "confirmed_duration_s", "planned_start_s", "planned_end_s"]
)
def test_confirmed_task_plan_is_immutable_while_progress_can_change(
    connection: psycopg.Connection[Any],
    task_context: dict[str, Any],
    column: str,
) -> None:
    task = insert(
        connection,
        "session_task",
        **task_context,
        duration_source="user_estimate",
        confirmed_duration_s=60,
    )
    connection.execute("SET CONSTRAINTS ALL IMMEDIATE")
    value: str | int = "recipe_rule" if column == "duration_source" else 30
    with pytest.raises(psycopg.errors.CheckViolation), connection.transaction():
        connection.execute(
            sql.SQL("UPDATE recipeweave.session_task SET {}=%s WHERE id=%s").format(
                sql.Identifier(column)
            ),
            (value, task),
        )
    connection.execute(
        "UPDATE recipeweave.session_task SET status='running', actual_start_at=now(), "
        "timer_started_at=now(), timer_duration_s=60 WHERE id=%s",
        (task,),
    )
    row = connection.execute(
        "SELECT status, duration_source, confirmed_duration_s "
        "FROM recipeweave.session_task WHERE id=%s",
        (task,),
    ).fetchone()
    assert row == ("running", "user_estimate", 60)


def test_seed_duration_upgrade_keeps_adopted_old_rule_and_changes_only_target_draft(
    connection: psycopg.Connection[Any], recipe: dict[str, UUID]
) -> None:
    source_id = UUID("9decf898-19cd-5c03-b3e2-947d838c06bd")
    old_rule = UUID("aa59a90d-0a79-5f69-95a9-7857ffe94fad")
    new_rule = UUID("9b2b5a4c-18db-5694-b175-96f9f2717e7c")
    target = UUID("fcb0b2fa-f387-5a51-8bed-0b8f0a539e36")
    if not connection.execute(
        "SELECT id FROM recipeweave.source_record WHERE id=%s", (source_id,)
    ).fetchone():
        insert(
            connection,
            "source_record",
            id=source_id,
            title="旧seed移行試験",
            locator="移行試験",
            retrieved_at=datetime.now(UTC),
            content_hash="1" * 64,
            license_note="調理試作なしの試験資料",
        )
    if not connection.execute(
        "SELECT id FROM recipeweave.scaling_rule WHERE id=%s", (old_rule,)
    ).fetchone():
        insert(
            connection,
            "scaling_rule",
            id=old_rule,
            name="工程時間は人数変更時に再確認",
            mode="manual",
            min_servings=1,
            max_servings=2,
            round_mode="none",
            round_increment="0.01",
            source_id=source_id,
        )
    if not connection.execute(
        "SELECT id FROM recipeweave.recipe_version WHERE id=%s", (target,)
    ).fetchone():
        insert(
            connection,
            "recipe_version",
            id=target,
            recipe_id=recipe["recipe"],
            version=2,
            release_id=recipe["release"],
            base_servings=2,
            output_amount=100,
            output_unit_id=recipe["unit"],
            status="draft",
            validation="pending",
            content_hash="2" * 64,
        )
    existing = connection.execute(
        "SELECT id FROM recipeweave.recipe_step WHERE recipe_version_id=%s "
        "ORDER BY step_no LIMIT 1",
        (target,),
    ).fetchone()
    if existing:
        step = existing[0]
        connection.execute(
            "UPDATE recipeweave.recipe_step SET scaling_rule_id=%s WHERE id=%s", (old_rule, step)
        )
    else:
        step = insert(
            connection,
            "recipe_step",
            recipe_version_id=target,
            step_no=1,
            operation_id=recipe["operation"],
            instruction="移行試験",
            attention="active",
            duration_min_s=30,
            duration_max_s=60,
            scaling_rule_id=old_rule,
            completion_cue="切り終わり",
        )
    migration = next(
        statement
        for statement in split_sql(
            (ROOT / "database/migrations/005_manual_duration.sql").read_text()
        )
        if "DO $$" in statement
    )
    connection.execute(migration)
    connection.execute(migration)
    connection.execute("SET CONSTRAINTS ALL IMMEDIATE")
    assert connection.execute(
        "SELECT scaling_rule_id FROM recipeweave.recipe_step WHERE id=%s", (step,)
    ).fetchone() == (new_rule,)
    assert connection.execute(
        "SELECT max_servings FROM recipeweave.scaling_rule WHERE id=%s", (old_rule,)
    ).fetchone() == (2,)
    assert connection.execute(
        "SELECT scaling_rule_id FROM recipeweave.recipe_step WHERE id=%s", (recipe["step"],)
    ).fetchone() == (recipe["rule"],)


@pytest.fixture
def recipe(connection: psycopg.Connection[Any]) -> dict[str, UUID]:
    release = insert(connection, "catalog_release", version=str(uuid4()), manifest_hash="0" * 64)
    unit = insert(
        connection,
        "unit",
        code=str(uuid4()),
        name="グラム",
        dimension="mass",
        factor=1,
        offset=0,
        status="active",
    )
    food = insert(
        connection,
        "food",
        code=str(uuid4()),
        name="試験食材",
        kind="basic",
        release_id=release,
        status="active",
    )
    form = insert(
        connection,
        "food_form",
        food_id=food,
        name="生",
        state="raw",
        base_unit_id=unit,
        quantity_basis="edible",
        status="active",
    )
    axis = insert(
        connection,
        "axis",
        code=str(uuid4()),
        name="料理型",
        purpose="generation",
        selection="single",
        release_id=release,
        status="active",
    )
    option = insert(
        connection,
        "axis_option",
        axis_id=axis,
        code="stir",
        label="炒め物",
        definition="炒める料理",
        status="active",
    )
    identity = insert(
        connection, "recipe", title="試験料理", family_option_id=option, status="draft"
    )
    version = insert(
        connection,
        "recipe_version",
        recipe_id=identity,
        version=1,
        release_id=release,
        base_servings=2,
        output_amount=100,
        output_unit_id=unit,
        status="draft",
        validation="pending",
        content_hash="1" * 64,
    )
    rule = insert(
        connection,
        "scaling_rule",
        name="比例",
        mode="linear",
        min_servings=1,
        max_servings=4,
        round_mode="none",
        round_increment=1,
    )
    operation = insert(
        connection,
        "operation",
        code=str(uuid4()),
        name="切る",
        definition="包丁で切る",
        precondition="洗浄済み",
        completion_cue="切り終わり",
        status="active",
    )
    ingredient = insert(
        connection,
        "recipe_ingredient",
        recipe_version_id=version,
        line_no=1,
        form_id=form,
        role="main",
        demand_kind="purchase",
        amount_mode="exact",
        amount=100,
        unit_id=unit,
        canonical_amount=100,
        scaling_rule_id=rule,
        optional=False,
    )
    step = insert(
        connection,
        "recipe_step",
        recipe_version_id=version,
        step_no=1,
        operation_id=operation,
        instruction="切ります",
        attention="active",
        duration_min_s=30,
        duration_max_s=60,
        scaling_rule_id=rule,
        completion_cue="切り終わり",
    )
    connection.execute("SET CONSTRAINTS ALL IMMEDIATE")
    connection.execute("SET CONSTRAINTS ALL DEFERRED")
    return dict(
        release=release,
        unit=unit,
        food=food,
        form=form,
        version=version,
        recipe=identity,
        rule=rule,
        operation=operation,
        ingredient=ingredient,
        step=step,
    )


def test_live_schema_has_original_tables_and_extension(connection: psycopg.Connection[Any]) -> None:
    actual = {
        row[0]
        for row in connection.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'recipeweave'"
        )
    }
    expected = {table["name"] for table in extract()["tables"]}
    assert expected | {"schema_migrations"} == actual
    assert connection.execute(
        "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
    ).fetchone()


def test_nonfinite_numeric_is_rejected(
    connection: psycopg.Connection[Any], recipe: dict[str, UUID]
) -> None:
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute(
            "UPDATE recipeweave.unit SET factor = 'NaN' WHERE id = %s", (recipe["unit"],)
        )


def test_range_requires_both_bounds(
    connection: psycopg.Connection[Any], recipe: dict[str, UUID]
) -> None:
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute(
            "UPDATE recipeweave.recipe_ingredient SET amount_mode='range', "
            "canonical_amount=NULL WHERE id=%s",
            (recipe["ingredient"],),
        )


def test_exact_conversion_requires_correct_canonical_amount(
    connection: psycopg.Connection[Any], recipe: dict[str, UUID]
) -> None:
    connection.execute(
        "UPDATE recipeweave.recipe_ingredient SET canonical_amount=99 WHERE id=%s",
        (recipe["ingredient"],),
    )
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute("SET CONSTRAINTS ALL IMMEDIATE")


def test_dependency_cycle_is_rejected(
    connection: psycopg.Connection[Any], recipe: dict[str, UUID]
) -> None:
    step = insert(
        connection,
        "recipe_step",
        recipe_version_id=recipe["version"],
        step_no=2,
        operation_id=recipe["operation"],
        instruction="盛ります",
        attention="active",
        duration_min_s=10,
        duration_max_s=10,
        scaling_rule_id=recipe["rule"],
        completion_cue="盛り終わり",
    )
    insert(
        connection,
        "step_dependency",
        before_step_id=recipe["step"],
        after_step_id=step,
        kind="sequence",
        min_lag_s=0,
    )
    insert(
        connection,
        "step_dependency",
        before_step_id=step,
        after_step_id=recipe["step"],
        kind="sequence",
        min_lag_s=0,
    )
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute("SET CONSTRAINTS ALL IMMEDIATE")


def test_cross_version_dependency_is_rejected(
    connection: psycopg.Connection[Any], recipe: dict[str, UUID]
) -> None:
    version = insert(
        connection,
        "recipe_version",
        recipe_id=recipe["recipe"],
        version=2,
        release_id=recipe["release"],
        base_servings=2,
        output_amount=100,
        output_unit_id=recipe["unit"],
        status="draft",
        validation="pending",
        content_hash="2" * 64,
    )
    step = insert(
        connection,
        "recipe_step",
        recipe_version_id=version,
        step_no=1,
        operation_id=recipe["operation"],
        instruction="盛ります",
        attention="active",
        duration_min_s=10,
        duration_max_s=10,
        scaling_rule_id=recipe["rule"],
        completion_cue="盛り終わり",
    )
    insert(
        connection,
        "step_dependency",
        before_step_id=recipe["step"],
        after_step_id=step,
        kind="sequence",
        min_lag_s=0,
    )
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute("SET CONSTRAINTS ALL IMMEDIATE")


def test_published_recipe_content_cannot_change(
    connection: psycopg.Connection[Any], recipe: dict[str, UUID]
) -> None:
    connection.execute(
        "UPDATE recipeweave.catalog_release SET published_at=NOW() WHERE id=%s",
        (recipe["release"],),
    )
    connection.execute(
        "UPDATE recipeweave.recipe_version SET status='published', "
        "validation='passed', published_at=now() WHERE id=%s",
        (recipe["version"],),
    )
    connection.execute("SET CONSTRAINTS ALL IMMEDIATE")
    assert (
        connection.execute(
            "SELECT count(*) FROM recipeweave.outbox_event WHERE aggregate_id=%s "
            "AND event_type='recipe_published'",
            (recipe["recipe"],),
        ).fetchone()[0]
        == 1
    )
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute(
            "UPDATE recipeweave.recipe_ingredient SET amount=200, canonical_amount=200 WHERE id=%s",
            (recipe["ingredient"],),
        )


def test_food_hierarchy_cycle_is_rejected(
    connection: psycopg.Connection[Any], recipe: dict[str, UUID]
) -> None:
    food = insert(
        connection,
        "food",
        code=str(uuid4()),
        name="子分類",
        kind="basic",
        release_id=recipe["release"],
        parent_id=recipe["food"],
        status="active",
    )
    connection.execute(
        "UPDATE recipeweave.food SET parent_id=%s WHERE id=%s", (food, recipe["food"])
    )
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute("SET CONSTRAINTS ALL IMMEDIATE")


def test_material_fraction_cannot_exceed_one(
    connection: psycopg.Connection[Any], recipe: dict[str, UUID]
) -> None:
    node = insert(
        connection,
        "material_node",
        recipe_version_id=recipe["version"],
        name="投入材料",
        kind="ingredient",
        ingredient_line_id=recipe["ingredient"],
    )
    step = insert(
        connection,
        "recipe_step",
        recipe_version_id=recipe["version"],
        step_no=2,
        operation_id=recipe["operation"],
        instruction="分けます",
        attention="active",
        duration_min_s=10,
        duration_max_s=10,
        scaling_rule_id=recipe["rule"],
        completion_cue="分割済み",
    )
    insert(connection, "step_input", step_id=recipe["step"], material_id=node, fraction="0.6")
    insert(connection, "step_input", step_id=step, material_id=node, fraction="0.6")
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute("SET CONSTRAINTS ALL IMMEDIATE")


def test_unknown_stock_is_null_not_zero(
    connection: psycopg.Connection[Any], recipe: dict[str, UUID]
) -> None:
    user = insert(
        connection,
        "app_user",
        auth_subject=str(uuid4()),
        state="active",
        locale="ja-JP",
        timezone="Asia/Tokyo",
    )
    lot = insert(
        connection,
        "pantry_lot",
        user_id=user,
        form_id=recipe["form"],
        unit_id=recipe["unit"],
        amount=None,
        quantity_quality="unknown",
    )
    connection.execute("SET CONSTRAINTS ALL IMMEDIATE")
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute("UPDATE recipeweave.pantry_lot SET amount=0 WHERE id=%s", (lot,))


def test_row_level_security_hides_other_users_private_food(
    connection: psycopg.Connection[Any], recipe: dict[str, UUID]
) -> None:
    first = insert(
        connection,
        "app_user",
        auth_subject=str(uuid4()),
        state="active",
        locale="ja-JP",
        timezone="Asia/Tokyo",
    )
    second = insert(
        connection,
        "app_user",
        auth_subject=str(uuid4()),
        state="active",
        locale="ja-JP",
        timezone="Asia/Tokyo",
    )
    first_release = insert(
        connection, "catalog_release", version=str(uuid4()), manifest_hash="0" * 64, owner_id=first
    )
    second_release = insert(
        connection, "catalog_release", version=str(uuid4()), manifest_hash="0" * 64, owner_id=second
    )
    first_food = insert(
        connection,
        "food",
        code=str(uuid4()),
        name="本人の食材",
        kind="basic",
        release_id=first_release,
        status="active",
        owner_id=first,
    )
    second_food = insert(
        connection,
        "food",
        code=str(uuid4()),
        name="他人の食材",
        kind="basic",
        release_id=second_release,
        status="active",
        owner_id=second,
    )
    second_form = insert(
        connection,
        "food_form",
        food_id=second_food,
        name="生",
        state="raw",
        base_unit_id=recipe["unit"],
        quantity_basis="edible",
        status="active",
    )
    connection.execute("SET CONSTRAINTS ALL IMMEDIATE")
    role = sql.Identifier("recipeweave_test_" + uuid4().hex)
    connection.execute(sql.SQL("CREATE ROLE {} NOLOGIN NOSUPERUSER NOBYPASSRLS").format(role))
    connection.execute(sql.SQL("GRANT USAGE ON SCHEMA recipeweave TO {}").format(role))
    connection.execute(
        sql.SQL(
            "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA recipeweave TO {}"
        ).format(role)
    )
    connection.execute(sql.SQL("SET LOCAL ROLE {}").format(role))
    connection.execute(
        "SELECT set_config('recipeweave.role', 'user', true), "
        "set_config('recipeweave.user_id', %s, true)",
        (str(first),),
    )
    visible = {
        row[0]
        for row in connection.execute(
            "SELECT id FROM recipeweave.food WHERE id = ANY(%s)",
            ([first_food, second_food, recipe["food"]],),
        )
    }
    assert visible == {first_food, recipe["food"]}
    assert (
        connection.execute(
            "SELECT id FROM recipeweave.food_form WHERE id=%s", (second_form,)
        ).fetchone()
        is None
    )
    assert (
        connection.execute("SELECT id FROM recipeweave.app_user WHERE id=%s", (second,)).fetchone()
        is None
    )
    with pytest.raises(psycopg.errors.InsufficientPrivilege):
        insert(
            connection,
            "pantry_lot",
            user_id=second,
            form_id=recipe["form"],
            unit_id=recipe["unit"],
            amount=1,
        )


def test_database_foreign_key_actions_match_ddl(connection: psycopg.Connection[Any]) -> None:
    actual = {
        (row[0], row[1]): (row[2], row[3], row[4])
        for row in connection.execute(
            "SELECT table_def.relname, constraint_def.conname, constraint_def.confdeltype, "
            "constraint_def.condeferrable, constraint_def.condeferred "
            "FROM pg_constraint constraint_def "
            "JOIN pg_class table_def ON table_def.oid=constraint_def.conrelid "
            "JOIN pg_namespace namespace_def ON namespace_def.oid=table_def.relnamespace "
            "WHERE namespace_def.nspname='recipeweave' AND constraint_def.contype='f'"
        )
    }
    codes = {"RESTRICT": "r", "CASCADE": "c", "SET NULL": "n"}
    for table in extract()["tables"]:
        for foreign in table["foreign_keys"]:
            assert actual[(table["name"], foreign["name"])] == (
                codes[foreign["on_delete"]],
                True,
                True,
            )


@pytest.mark.parametrize("preserve_kind", ["none", "edited", "consumed"])
def test_receipt_undo_preserves_only_edited_or_consumed_lots(
    connection: psycopg.Connection[Any], recipe: dict[str, UUID], preserve_kind: str
) -> None:
    user = insert(
        connection,
        "app_user",
        auth_subject=str(uuid4()),
        state="active",
        locale="ja-JP",
        timezone="Asia/Tokyo",
    )
    receipt = insert(connection, "receipt_import", user_id=user, idempotency_key=str(uuid4()))
    lot = insert(
        connection,
        "pantry_lot",
        user_id=user,
        form_id=recipe["form"],
        amount=2,
        unit_id=recipe["unit"],
        source_import_id=receipt,
        original_form_id=recipe["form"],
        original_amount=2,
        original_unit_id=recipe["unit"],
        edited=preserve_kind == "edited",
    )
    insert(
        connection,
        "receipt_line",
        import_id=receipt,
        line_no=1,
        raw_name="試験食材",
        form_id=recipe["form"],
        amount=2,
        unit_id=recipe["unit"],
        decision="accepted",
        pantry_lot_id=lot,
    )
    connection.execute(
        "UPDATE recipeweave.receipt_import SET status='committed', "
        "revision=2, committed_at=NOW() WHERE id=%s",
        (receipt,),
    )
    if preserve_kind == "consumed":
        menu = insert(connection, "menu", user_id=user, name="試験献立", servings=1, revision=1)
        session = insert(
            connection,
            "cooking_session",
            menu_id=menu,
            menu_revision=1,
            status="planned",
            planner_version="test-v1",
            input_snapshot='{"schema_version":1,"menu_revision":1,"items":[],"ingredients":[],"resources":[],"planner_config":{}}',
            input_hash="0" * 64,
        )
        connection.execute("UPDATE recipeweave.pantry_lot SET amount=1 WHERE id=%s", (lot,))
        insert(
            connection,
            "pantry_consumption",
            user_id=user,
            session_id=session,
            lot_id=lot,
            amount=1,
            unit_id=recipe["unit"],
        )
    if preserve_kind == "none":
        connection.execute("UPDATE recipeweave.pantry_lot SET status='undone' WHERE id=%s", (lot,))
    connection.execute(
        "UPDATE recipeweave.receipt_import SET status='reverted', "
        "revision=3, reverted_at=NOW() WHERE id=%s",
        (receipt,),
    )
    connection.execute("SET CONSTRAINTS ALL IMMEDIATE")
    result = connection.execute(
        "SELECT undo_preserved_count FROM recipeweave.receipt_import WHERE id=%s", (receipt,)
    ).fetchone()
    assert result == (0 if preserve_kind == "none" else 1,)
    assert connection.execute(
        "SELECT status FROM recipeweave.pantry_lot WHERE id=%s", (lot,)
    ).fetchone() == ("undone" if preserve_kind == "none" else "active",)


def test_receipt_undo_cannot_leave_untouched_inventory(
    connection: psycopg.Connection[Any], recipe: dict[str, UUID]
) -> None:
    user = insert(
        connection,
        "app_user",
        auth_subject=str(uuid4()),
        state="active",
        locale="ja-JP",
        timezone="Asia/Tokyo",
    )
    receipt = insert(connection, "receipt_import", user_id=user, idempotency_key=str(uuid4()))
    lot = insert(
        connection,
        "pantry_lot",
        user_id=user,
        form_id=recipe["form"],
        amount=2,
        unit_id=recipe["unit"],
        source_import_id=receipt,
    )
    insert(
        connection,
        "receipt_line",
        import_id=receipt,
        line_no=1,
        raw_name="試験食材",
        form_id=recipe["form"],
        amount=2,
        unit_id=recipe["unit"],
        decision="accepted",
        pantry_lot_id=lot,
    )
    connection.execute(
        "UPDATE recipeweave.receipt_import SET status='committed', "
        "revision=2, committed_at=NOW() WHERE id=%s",
        (receipt,),
    )
    connection.execute(
        "UPDATE recipeweave.receipt_import SET status='reverted', "
        "revision=3, reverted_at=NOW() WHERE id=%s",
        (receipt,),
    )
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute("SET CONSTRAINTS ALL IMMEDIATE")


def test_live_column_types_nullability_defaults_match_catalog(
    connection: psycopg.Connection[Any],
) -> None:
    rows = connection.execute(
        "SELECT c.relname, a.attname, format_type(a.atttypid,a.atttypmod), "
        "a.attnotnull, pg_get_expr(d.adbin,d.adrelid) "
        "FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace "
        "JOIN pg_attribute a ON a.attrelid=c.oid "
        "LEFT JOIN pg_attrdef d ON d.adrelid=c.oid AND d.adnum=a.attnum "
        "WHERE n.nspname='recipeweave' AND c.relkind='r' AND a.attnum>0 AND NOT a.attisdropped"
    )
    actual = {(row[0], row[1]): row[2:] for row in rows}
    for table in extract()["tables"]:
        for column in table["columns"]:
            datatype, nonnull, default = actual[(table["name"], column["name"])]
            datatype = datatype.replace("character(", "char(").replace(
                "timestamp with time zone", "timestamptz"
            )
            assert datatype == column["type"]
            assert nonnull is not column["nullable"]
            expected_default = column["default"]
            if expected_default is None:
                assert default is None
            else:
                assert default.lower().replace("::text", "") == expected_default.lower()


@pytest.mark.parametrize(
    ("table", "column", "limit"),
    [
        ("food", "name", 100),
        ("food_alias", "alias", 500),
        ("food_form", "name", 500),
        ("recipe", "title", 500),
        ("recipe_version", "description", 5000),
        ("recipe_step", "title", 500),
        ("recipe_step", "instruction", 5000),
        ("recipe_ingredient", "note", 500),
        ("resource_type", "name", 500),
        ("axis_option", "label", 500),
    ],
)
def test_catalog_display_text_limits_preserve_boundary_and_reject_overflow(
    connection: psycopg.Connection[Any],
    recipe: dict[str, UUID],
    table: str,
    column: str,
    limit: int,
) -> None:
    identifiers = {
        "food": recipe["food"],
        "food_form": recipe["form"],
        "recipe": recipe["recipe"],
        "recipe_version": recipe["version"],
        "recipe_step": recipe["step"],
        "recipe_ingredient": recipe["ingredient"],
    }
    if table == "food_alias":
        identity = insert(
            connection, table, food_id=recipe["food"], alias="試験別名", locale="ja-JP"
        )
    elif table == "resource_type":
        identity = insert(connection, table, code=str(uuid4()), name="試験道具", status="active")
    elif table == "axis_option":
        row = connection.execute(
            "SELECT family_option_id FROM recipeweave.recipe WHERE id=%s", (recipe["recipe"],)
        ).fetchone()
        assert row is not None
        identity = row[0]
    else:
        identity = identifiers[table]
    statement = sql.SQL("UPDATE recipeweave.{} SET {}=%s WHERE id=%s").format(
        sql.Identifier(table), sql.Identifier(column)
    )
    boundary = "あ" * limit
    connection.execute(statement, (boundary, identity))
    actual = connection.execute(
        sql.SQL("SELECT {} FROM recipeweave.{} WHERE id=%s").format(
            sql.Identifier(column), sql.Identifier(table)
        ),
        (identity,),
    ).fetchone()
    assert actual == (boundary,)
    metadata = next(item for item in extract()["tables"] if item["name"] == table)
    assert (
        next(item for item in metadata["columns"] if item["name"] == column)["max_length"] == limit
    )
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute(statement, (boundary + "い", identity))
