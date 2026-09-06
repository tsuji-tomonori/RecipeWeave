"""本人の正規化バックアップに限定した型と固定SQLをDDLから生成する。"""

import argparse
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.generate_entity_apis import field_line, load_tables, pascal, scope  # noqa: E402

API = ROOT / "backend/src/app/apis/backup"
PACKAGE = ROOT / "backend/src/app/backup"
HEADER = "# generate_backup_api.py による自動生成。直接編集しない。\n"
OWNED = [
    "user_preference",
    "user_exclusion",
    "user_recipe_event",
    "menu",
    "menu_item",
    "menu_ingredient_override",
    "kitchen_resource",
    "cooking_session",
    "session_task",
    "task_dependency",
    "resource_reservation",
    "ingredient_total",
    "pantry_lot",
    "shopping_item",
    "receipt_import",
    "receipt_line",
    "user_food",
    "user_pantry_food",
    "pantry_consumption",
    "user_shopping_check",
]
PRIVATE = [
    "catalog_release",
    "food",
    "food_alias",
    "food_form",
    "food_axis_option",
    "product",
    "conversion",
    "food_allergen",
    "product_version",
    "product_component",
    "product_allergen",
    "product_preparation_rule",
    "nutrition_fact",
    "form_yield",
]
DELETE_ORDER = [
    "resource_reservation",
    "task_dependency",
    "shopping_item",
    "pantry_consumption",
    "receipt_line",
    "menu_ingredient_override",
    "session_task",
    "ingredient_total",
    "cooking_session",
    "menu_item",
    "menu",
    "kitchen_resource",
    "pantry_lot",
    "receipt_import",
    "user_preference",
    "user_exclusion",
    "user_recipe_event",
    "user_food",
    "user_pantry_food",
    "user_shopping_check",
    "product_preparation_rule",
    "product_allergen",
    "nutrition_fact",
    "food_allergen",
    "form_yield",
    "conversion",
    "product_component",
    "product_version",
    "product",
    "food_axis_option",
    "food_alias",
    "food_form",
    "food",
    "catalog_release",
]
INSERT_ORDER = [
    "catalog_release",
    "food",
    "food_form",
    "food_alias",
    "food_axis_option",
    "product",
    "product_version",
    "product_component",
    "conversion",
    "food_allergen",
    "product_allergen",
    "product_preparation_rule",
    "nutrition_fact",
    "form_yield",
    "user_preference",
    "user_exclusion",
    "user_recipe_event",
    "menu",
    "menu_item",
    "menu_ingredient_override",
    "kitchen_resource",
    "cooking_session",
    "session_task",
    "task_dependency",
    "resource_reservation",
    "ingredient_total",
    "shopping_item",
    "receipt_import",
    "pantry_lot",
    "receipt_line",
    "user_food",
    "user_pantry_food",
    "pantry_consumption",
    "user_shopping_check",
]


def private_scope(name: str, *, common: bool = False, alias: str = "t") -> str:
    """私有食品の明示した14表だけを、根のfood所有者へたどる。"""
    owner = "IS NULL" if common else "= %(actor_id)s"
    if name in {"catalog_release", "food"}:
        return f"{alias}.owner_id {owner}"
    if name in {"food_alias", "food_form", "food_axis_option", "product"}:
        source = f"food.id = {alias}.food_id"
        joins = ""
    elif name in {"conversion", "food_allergen", "form_yield"}:
        column = "input_form_id" if name == "form_yield" else "form_id"
        source = f"form.id = {alias}.{column}"
        joins = " INNER JOIN recipeweave.food_form AS form ON form.food_id = food.id"
    elif name == "product_version":
        source = f"product.id = {alias}.product_id"
        joins = " INNER JOIN recipeweave.product AS product ON product.food_id = food.id"
    elif name == "nutrition_fact":
        return (
            "EXISTS (SELECT 1 FROM recipeweave.food AS food "
            "INNER JOIN recipeweave.food_form AS form ON form.food_id = food.id "
            f"WHERE form.id = {alias}.form_id AND food.owner_id {owner}) OR "
            "EXISTS (SELECT 1 FROM recipeweave.food AS food "
            "INNER JOIN recipeweave.product AS product ON product.food_id = food.id "
            "INNER JOIN recipeweave.product_version AS version ON version.product_id = product.id "
            f"WHERE version.id = {alias}.product_version_id AND food.owner_id {owner})"
        )
    else:
        source = f"version.id = {alias}.product_version_id"
        joins = (
            " INNER JOIN recipeweave.product AS product ON product.food_id = food.id"
            " INNER JOIN recipeweave.product_version AS version ON version.product_id = product.id"
        )
    return (
        f"EXISTS (SELECT 1 FROM recipeweave.food AS food{joins} "
        f"WHERE {source} AND food.owner_id {owner})"
    )


def render() -> dict[Path, str]:
    """列集合、所有者経路、固定した依存順を元に全生成物を作る。"""
    tables = {table["name"]: table for table in load_tables()}
    names = OWNED + PRIVATE
    assert set(names) == set(DELETE_ORDER) == set(INSERT_ORDER)
    outputs: dict[Path, str] = {}
    models = (
        HEADER
        + """from decimal import Decimal
from typing import Literal
from uuid import UUID
from pydantic import AwareDatetime, Field
from datetime import date
from app.entities.json_contracts import BigInteger, ContractModel, CookingInput, ProductPreparation

"""
    )
    metadata: dict[str, Any] = {}
    scopes: dict[str, str] = {}
    projections: list[str] = []
    for name in names:
        table = tables[name]
        for column in table["columns"]:
            column["table"] = name
        models += f"class {pascal(name)}BackupRow(ContractModel):\n"
        models += f'    """{table["description"]}の全列。ID・作成時刻も元の値を保持する。"""\n\n'
        models += "".join(field_line(column) for column in table["columns"]) + "\n\n"
        scopes[name] = private_scope(name) if name in PRIVATE else scope(table, tables)
        metadata[name] = {
            "label": table["description"],
            "columns": [column["name"] for column in table["columns"]],
            "json_columns": [
                column["name"] for column in table["columns"] if column["type"] == "jsonb"
            ],
            "bigint_columns": [
                column["name"] for column in table["columns"] if column["type"] == "bigint"
            ],
            "references": [
                {"column": fk["columns"][0], "table": fk["referenced_table"]}
                for fk in table["foreign_keys"]
            ],
        }
        pairs = []
        for column in table["columns"]:
            expr = f"t.{column['name']}"
            if column["type"].startswith("numeric") or column["type"] == "bigint":
                expr += "::TEXT"
            pairs.append(f"'{column['name']}', {expr}")
        projections.append(
            "    (SELECT COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(\n        "
            + ",\n        ".join(pairs)
            + f") ORDER BY t.id), '[]'::JSONB)\n     FROM recipeweave.{name} AS t "
            + f"WHERE ({scopes[name]})) AS rows_{name}"
        )
    models += (
        "class BackupTables(ContractModel):\n"
        '    """一部省略による意図しない消去を避け、全34表を必須にする。"""\n\n'
    )
    models += "".join(
        f"    {name}: list[{pascal(name)}BackupRow] = Field(max_length=100000)\n" for name in names
    )
    outputs[PACKAGE / "models.py"] = models.translate(
        str.maketrans({"（": "(", "）": ")", "×": "x", "：": ":"})
    )
    outputs[PACKAGE / "inventory.py"] = (
        HEADER
        + "from typing import Any\n"
        + f"TABLES: dict[str, Any] = {metadata!r}\n"
        + f"OWNED: tuple[str, ...] = {tuple(OWNED)!r}\n"
        + f"PRIVATE: tuple[str, ...] = {tuple(PRIVATE)!r}\n"
        + f"DELETE_ORDER: tuple[str, ...] = {tuple(DELETE_ORDER)!r}\n"
        + f"INSERT_ORDER: tuple[str, ...] = {tuple(INSERT_ORDER)!r}\n"
    )
    export_sql = (
        "-- 本人の業務行と私有食品の全列を一つの読取スナップショットで取得する。\nSELECT\n"
        + ",\n".join(projections)
        + ";\n"
    )
    for operation in ("export_backup", "preview_backup", "restore_backup"):
        directory = API / operation / "sql"
        outputs[directory / "q010_export_tables.sql"] = export_sql
        outputs[directory / "q001_lock_revision.sql"] = (
            "-- 本人の更新版をロックし、確認と置換の間の更新を検出する。\n"
            "SELECT revision FROM recipeweave.workspace_revision\n"
            "WHERE user_id = %(actor_id)s FOR UPDATE;\n"
        )
        outputs[directory / "q002_profile.sql"] = (
            "-- 認証主体・状態を含めず、復元できる本人の表示設定だけを読む。\n"
            "SELECT locale, timezone FROM recipeweave.app_user WHERE id = %(actor_id)s;\n"
        )
        if operation == "export_backup":
            continue
        for name in names:
            outputs[directory / f"q100_delete_{name}.sql"] = (
                f"-- 全置換の確認対象である本人の{tables[name]['description']}だけを削除する。\n"
                f"DELETE FROM recipeweave.{name} AS t WHERE ({scopes[name]});\n"
            )
            columns = metadata[name]["columns"]
            outputs[directory / f"q200_insert_{name}.sql"] = (
                f"-- 検証済みバックアップの{tables[name]['description']}を元IDと全列で復元する。\n"
                f"INSERT INTO recipeweave.{name} (\n    "
                + ",\n    ".join(columns)
                + "\n) VALUES (\n    "
                + ",\n    ".join(f"%({column})s" for column in columns)
                + "\n);\n"
            )
        reference_tables = sorted(
            {ref["table"] for item in metadata.values() for ref in item["references"]}
        )
        for name in reference_tables:
            if name in OWNED or name == "app_user":
                continue
            allowed = private_scope(name, common=True) if name in PRIVATE else "TRUE"
            outputs[directory / f"q300_reference_{name}.sql"] = (
                "-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。\n"
                f"SELECT t.id FROM recipeweave.{name} AS t\n"
                f"WHERE t.id = ANY(%(reference_ids)s::UUID[]) AND ({allowed});\n"
            )
        outputs[directory / "q800_constraints_immediate.sql"] = (
            "-- 保存直前に遅延FK・制約トリガーをすべて検証する。\nSET CONSTRAINTS ALL IMMEDIATE;\n"
        )
        outputs[directory / "q801_constraints_deferred.sql"] = (
            "-- 復元する依存行の挿入順を組み立てる間は遅延可能な制約を保留する。\n"
            "SET CONSTRAINTS ALL DEFERRED;\n"
        )
        outputs[directory / "q802_restore_profile.sql"] = (
            "-- 本人の言語とタイムゾーンだけを復元し、認証主体とアカウント状態は保持する。\n"
            "UPDATE recipeweave.app_user SET locale = %(locale)s, timezone = %(timezone)s\n"
            "WHERE id = %(actor_id)s;\n"
        )
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = render()
    with TemporaryDirectory(prefix="backup-api-") as temporary:
        scratch = Path(temporary)
        targets: dict[Path, Path] = {}
        identical_sql: dict[str, Path] = {}
        for path, text in outputs.items():
            if path.suffix == ".sql" and text in identical_sql:
                targets[path] = identical_sql[text]
                continue
            target = scratch / path.relative_to(ROOT)
            targets[path] = target
            if path.suffix == ".sql":
                identical_sql[text] = target
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
        sql_result = subprocess.run(
            [
                "sqlfluff",
                "fix",
                "--force",
                "--config",
                str(ROOT / ".sqlfluff"),
                "--processes",
                "4",
                str(scratch),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if sql_result.returncode:
            Path("/tmp/backup-sql-fix.log").write_text(sql_result.stdout + sql_result.stderr)
            linted = subprocess.run(
                [
                    "sqlfluff",
                    "lint",
                    "--config",
                    str(ROOT / ".sqlfluff"),
                    "--processes",
                    "4",
                    "--format",
                    "json",
                    str(scratch),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if linted.returncode:
                Path("/tmp/backup-sql-lint.json").write_text(linted.stdout)
                failed = next(path for path in outputs if path.name == "q010_export_tables.sql")
                Path("/tmp/backup-export-formatted.sql").write_text(targets[failed].read_text())
                raise ValueError("バックアップSQL解析失敗: /tmp/backup-sql-lint.json")
        subprocess.run(
            [
                "ruff",
                "check",
                "--fix",
                "--config",
                str(ROOT / "backend/pyproject.toml"),
                "--config",
                'lint.isort.known-first-party=["app"]',
                str(scratch),
            ],
            check=False,
            capture_output=True,
        )
        subprocess.run(
            ["ruff", "format", "--config", str(ROOT / "backend/pyproject.toml"), str(scratch)],
            check=True,
            capture_output=True,
        )
        for path in outputs:
            outputs[path] = targets[path].read_text()
    changed = [
        path for path, text in outputs.items() if not path.exists() or path.read_text() != text
    ]
    if args.check:
        if changed:
            print("\n".join(str(path.relative_to(ROOT)) for path in changed))
            return 1
    else:
        for path, text in outputs.items():
            if path.is_symlink():
                raise ValueError("生成先symlinkは使用できません")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    print(f"バックアップ型・SQL生成: {len(outputs)}ファイル")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
