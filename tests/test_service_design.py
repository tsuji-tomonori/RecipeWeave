"""実装変更への追従と、誤った設計書を生成しない境界を検査する。"""

import ast
import copy
import shutil
from pathlib import Path

import pytest
from app.main import create_app

from tools.design.api import load_operations, restrictions, schema_rows, validate_references
from tools.design.common import DesignError
from tools.design.database import load_tables, parse_one, project_table, query_projection
from tools.design.flow import block, render_expression, validate_tree
from tools.design.storage import synchronize
from tools.generate_service_design import ROOT, build_outputs


@pytest.fixture
def openapi() -> dict:
    return create_app().openapi()


def test_actual_inventory_and_all_operation_documents(openapi: dict) -> None:
    operations = load_operations(ROOT, openapi)
    assert {"get_health", "list_foods", "list_recipes", "get_recipe"} <= {
        op.id for op in operations
    }
    tables = load_tables(ROOT)
    assert len(tables) >= 71
    assert {"recipeweave.recipe", "recipeweave.food", "recipeweave.app_user"} <= set(tables)
    outputs = build_outputs()
    assert outputs == build_outputs()
    for op in operations:
        for kind in ("interface", "sequence", "queries", "detail", "messages", "tests"):
            assert f"api/operations/{op.id}/{kind}.md" in outputs
    assert "||--" in outputs["database/ER.md"]
    assert "recipeweave.recipe" in outputs["api/CRUD.md"]
    assert "SQL" in outputs["api/operations/get_recipe/queries.md"]
    assert "ログメッセージ" in outputs["api/operations/get_health/messages.md"]
    assert "workspace/get_workspace/sql/" in outputs["api/operations/create_pantry_lot/queries.md"]
    assert "recipes/get_recipe/sql/" in outputs["api/operations/preview_cooking_plan/queries.md"]


def test_ddl_change_requires_column_meaning(tmp_path: Path) -> None:
    shutil.copytree(ROOT / "database", tmp_path / "database")
    shutil.copytree(ROOT / "spec/database", tmp_path / "spec/database")
    path = tmp_path / "database/migrations/002_relational_schema.sql"
    path.write_text(
        path.read_text().replace("    title TEXT NOT NULL,", "    title BIGINT NOT NULL,", 1)
    )
    with pytest.raises((DesignError, ValueError), match="原設計"):
        load_tables(tmp_path)


def test_ddl_preserves_null_default_and_table_primary_key() -> None:
    ddl = "CREATE TABLE a.t (id BIGINT, value TEXT DEFAULT 'x', PRIMARY KEY (id));"
    item = project_table(parse_one(ddl, "fixture"), "fixture")
    assert item is not None
    assert [(c.name, c.nullable, c.default) for c in item.columns] == [
        ("id", False, "なし"),
        ("value", True, "'x'"),
    ]
    assert "PRIMARY KEY (id)" in item.constraints


@pytest.mark.parametrize(
    "text",
    [
        "ALTER TABLE a.t ADD COLUMN value TEXT;",
        "DROP TABLE a.t;",
        "CREATE TABLE a.t (id INT); CREATE TABLE a.u (id INT);",
    ],
)
def test_unsupported_ddl_fails_instead_of_silent_omission(text: str) -> None:
    with pytest.raises(DesignError):
        project_table(parse_one(text, "fixture"), "fixture")


@pytest.mark.parametrize(
    "text",
    [
        "SELECT unknown FROM recipeweave.user_state;",
        "SELECT subject FROM recipeweave.unknown;",
        "SELECT * FROM recipeweave.user_state;",
        "INSERT INTO recipeweave.user_state (unknown) VALUES (1);",
        "SELECT subject FROM recipeweave.user_state; DELETE FROM recipeweave.user_state;",
    ],
)
def test_invalid_sql_cannot_produce_crud(text: str) -> None:
    with pytest.raises(DesignError):
        query_projection(text, "fixture", "test", load_tables(ROOT))


def test_crud_distinguishes_write_target_and_read_source() -> None:
    tables = load_tables(ROOT)
    query = query_projection(
        "INSERT INTO recipeweave.user_state (subject) "
        "SELECT id FROM recipeweave.schema_migrations;",
        "fixture",
        "test",
        tables,
    )
    assert query.actions == {
        "recipeweave.user_state": {"C"},
        "recipeweave.schema_migrations": {"R"},
    }
    update = query_projection(
        "UPDATE recipeweave.user_state SET revision = %(revision)s "
        "WHERE subject = %(subject)s RETURNING revision;",
        "fixture",
        "test",
        tables,
    )
    assert update.actions == {"recipeweave.user_state": {"U"}}
    assert update.parameters == ["revision", "subject"]


@pytest.mark.parametrize("mutation", ["path", "error", "authentication", "id", "reference"])
def test_openapi_mismatch_stops_generation(openapi: dict, mutation: str) -> None:
    spec = copy.deepcopy(openapi)
    operation = spec["paths"]["/api/recipes/{recipe_id}"]["get"]
    if mutation == "path":
        operation["parameters"] = []
    elif mutation == "error":
        operation["responses"]["418"] = {"description": "未定義エラー"}
    elif mutation == "authentication":
        operation["security"] = [{"HTTPBearer": []}]
    elif mutation == "id":
        operation["operationId"] = "get_health"
    else:
        operation["responses"]["200"]["content"]["application/json"]["schema"] = {
            "$ref": "#/components/schemas/DoesNotExist"
        }
    with pytest.raises(DesignError):
        load_operations(ROOT, spec)


def test_schema_preserves_required_nullable_enum_and_references() -> None:
    spec = {
        "components": {
            "schemas": {
                "State": {
                    "type": "object",
                    "required": ["revision"],
                    "properties": {
                        "revision": {"type": "integer", "minimum": 0},
                        "status": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "enum": ["active", None],
                        },
                    },
                }
            }
        }
    }
    rows = schema_rows({"$ref": "#/components/schemas/State"}, spec)
    assert rows[0][2:4] == ["必須", "minimum=0"]
    assert rows[1][1:4] == ["anyOf(string, null)", "任意", 'enum=["active", null]']
    with pytest.raises(DesignError, match="外部OpenAPI"):
        validate_references({"$ref": "https://example.invalid/schema"}, spec)


def test_flow_retains_branch_loop_and_early_exit() -> None:
    tree = ast.parse("""def execute(values):
    for value in values:
        if value:
            return save(value)
        else:
            continue
    raise ValueError('empty')
    unreachable()
""")
    fn = tree.body[0]
    validate_tree(fn, "fixture")
    text = "\n".join(block(fn.body, "fixture"))
    assert "loop value in values" in text and "alt value" in text
    assert "関数終了: return" in text and "関数終了: raise" in text
    assert "次の反復へ進む" in text
    assert "unreachable" not in text


def test_conditional_expression_is_not_flattened_into_unconditional_calls() -> None:
    value = ast.parse("allow() and execute()", mode="eval").body
    text = "\n".join(render_expression(value))
    assert "条件付き式" in text and "allow() and execute()" in text
    assert "->>" not in text


@pytest.mark.parametrize(
    "source",
    [
        "def f(value):\n    match value:\n        case 1: go()\n",
        "def f():\n    return factory()()\n",
    ],
)
def test_unsupported_flow_fails(source: str) -> None:
    with pytest.raises(DesignError):
        validate_tree(ast.parse(source), "fixture")


def test_check_never_writes_and_write_removes_stale_owned_files(tmp_path: Path) -> None:
    outputs = {"README.md": "一覧\n", "api/old.md": "旧仕様\n"}
    synchronize(tmp_path, outputs, check=False)
    independent = tmp_path / "generator.md"
    independent.write_text("別生成器の管理対象\n")
    before = {str(p): (p.read_bytes(), p.stat().st_mtime_ns) for p in tmp_path.rglob("*.md")}
    replacement = {"README.md": "更新\n", "api/new.md": "新仕様\n"}
    with pytest.raises(DesignError, match="差分"):
        synchronize(tmp_path, replacement, check=True)
    assert before == {
        str(p): (p.read_bytes(), p.stat().st_mtime_ns) for p in tmp_path.rglob("*.md")
    }
    synchronize(tmp_path, replacement, check=False)
    assert not (tmp_path / "api/old.md").exists()
    assert independent.read_text() == "別生成器の管理対象\n"
    synchronize(tmp_path, replacement, check=True)


def test_symlink_and_path_escape_are_rejected_before_writing(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.mkdir()
    directory = tmp_path / "docs"
    directory.mkdir()
    (directory / "api").symlink_to(target, target_is_directory=True)
    for outputs in ({"api/x.md": "危険"}, {"../target/x.md": "危険"}):
        with pytest.raises(DesignError):
            synchronize(directory, outputs, check=False)
    assert not list(target.iterdir())


def test_manifest_output_hashes_and_relative_links() -> None:
    import hashlib
    import re

    outputs = build_outputs()
    manifest = outputs["MANIFEST.md"]
    for name, content in outputs.items():
        if name != "MANIFEST.md":
            assert hashlib.sha256(content.encode()).hexdigest() in manifest
        for link in re.findall(r"\]\(([^)]+)\)", content):
            if link.startswith(("https:", "http:", "#")):
                continue
            resolved = (ROOT / "docs/design/generated" / name).parent / link.split("#")[0]
            relative = (
                str(resolved.resolve().relative_to(ROOT / "docs/design/generated"))
                if (resolved.resolve().is_relative_to(ROOT / "docs/design/generated"))
                else None
            )
            assert relative in outputs or resolved.exists(), (name, link)


def test_nullable_branch_constraints_are_visible_in_the_table() -> None:
    value = restrictions(
        {"anyOf": [{"type": "integer", "minimum": 1, "maximum": 60}, {"type": "null"}]}
    )
    assert "minimum=1" in value and "maximum=60" in value and "integer" in value


def test_inline_foreign_key_requires_explicit_supported_projection() -> None:
    with pytest.raises(DesignError, match="REFERENCES"):
        project_table(
            parse_one("CREATE TABLE a.t (id INT REFERENCES a.u(id));", "fixture"), "fixture"
        )


@pytest.mark.parametrize(
    "text",
    [
        "WITH changed AS (DELETE FROM recipeweave.user_state RETURNING subject) "
        "SELECT subject FROM changed;",
    ],
)
def test_unsupported_combined_sql_cannot_hide_extra_side_effects(text: str) -> None:
    with pytest.raises(DesignError):
        query_projection(text, "fixture", "test", load_tables(ROOT))


def test_flow_retains_transaction_and_exception_handlers() -> None:
    source = """def execute():
    try:
        with connection.transaction():
            return save()
    except ValueError:
        raise RuntimeError('conflict')
    finally:
        close()
"""
    tree = ast.parse(source)
    validate_tree(tree, "fixture")
    diagram = "\n".join(block(tree.body[0].body, "fixture"))
    assert "context開始" in diagram
    assert "context終了" in diagram
    assert "opt 例外: ValueError" in diagram
    assert "finally" in diagram


def test_postgres_ast_detects_catalog_index_omission() -> None:
    from database.schema_catalog import extract
    from tools.design.postgres import inspect_postgres

    catalog = extract(ROOT)
    table = next(item for item in catalog["tables"] if item["indexes"])
    table["indexes"].pop()
    with pytest.raises(DesignError, match="索引集合"):
        inspect_postgres(ROOT, catalog)


def test_standalone_openapi_closes_only_reachable_references(openapi: dict) -> None:
    from tools.design.api import standalone_openapi

    operation = next(op for op in load_operations(ROOT, openapi) if op.id == "get_health")
    standalone = standalone_openapi(operation, openapi)
    validate_references(standalone, standalone)
    assert set(standalone["paths"]) == {"/api/health"}
    assert "AppSnapshot" not in standalone["components"].get("schemas", {})


def test_read_only_ctes_preserve_physical_table_lineage() -> None:
    query = query_projection(
        "WITH rows AS (SELECT subject FROM recipeweave.user_state) "
        "SELECT subject FROM rows WHERE subject = %(subject)s;",
        "fixture",
        "test",
        load_tables(ROOT),
    )
    assert query.actions == {"recipeweave.user_state": {"R"}}
    assert query.columns == {"recipeweave.user_state": ["subject"]}


def test_upsert_preserves_create_update_and_conflicting_column_lineage() -> None:
    query = query_projection(
        "INSERT INTO recipeweave.user_state AS current_state (subject, revision) "
        "VALUES (%(subject)s, 1) ON CONFLICT (subject) DO UPDATE SET "
        "revision = current_state.revision + EXCLUDED.revision RETURNING revision;",
        "fixture",
        "test",
        load_tables(ROOT),
    )
    assert query.actions == {"recipeweave.user_state": {"C", "U"}}
    assert query.columns == {"recipeweave.user_state": ["revision", "subject"]}
    with pytest.raises(DesignError, match="列"):
        query_projection(
            "INSERT INTO recipeweave.user_state (subject) VALUES ('x') "
            "ON CONFLICT (subject) DO UPDATE SET revision = EXCLUDED.unknown;",
            "fixture",
            "test",
            load_tables(ROOT),
        )


def test_lock_alias_is_validated_without_becoming_a_physical_table() -> None:
    tables = load_tables(ROOT)
    query = query_projection(
        "SELECT current_state.subject FROM recipeweave.user_state AS current_state "
        "FOR SHARE OF current_state;",
        "fixture",
        "test",
        tables,
    )
    assert query.actions == {"recipeweave.user_state": {"R"}}
    assert "FOR SHARE OF current_state" in query.sql
    with pytest.raises(DesignError, match="行ロック"):
        query_projection(
            "SELECT subject FROM recipeweave.user_state FOR UPDATE OF missing;",
            "fixture",
            "test",
            tables,
        )


def test_openapi_json_is_managed_without_deleting_unrelated_json(tmp_path: Path) -> None:
    outputs = {"api/operations/test/interface.openapi.json": "{}\n"}
    synchronize(tmp_path, outputs, check=False)
    synchronize(tmp_path, outputs, check=True)
    with pytest.raises(DesignError, match="管理対象外"):
        synchronize(tmp_path, {"api/arbitrary.json": "{}"}, check=False)
