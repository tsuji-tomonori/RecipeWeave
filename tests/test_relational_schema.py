"""原設計の網羅性とPostgreSQLで拒否すべき関係・ライフサイクルを検証する。"""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
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
        "UPDATE recipeweave.receipt_import SET status='committed', revision=2, committed_at=NOW() WHERE id=%s",
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
        "UPDATE recipeweave.receipt_import SET status='reverted', revision=3, reverted_at=NOW() WHERE id=%s",
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
        "UPDATE recipeweave.receipt_import SET status='committed', revision=2, committed_at=NOW() WHERE id=%s",
        (receipt,),
    )
    connection.execute(
        "UPDATE recipeweave.receipt_import SET status='reverted', revision=3, reverted_at=NOW() WHERE id=%s",
        (receipt,),
    )
    with pytest.raises(psycopg.errors.CheckViolation):
        connection.execute("SET CONSTRAINTS ALL IMMEDIATE")
