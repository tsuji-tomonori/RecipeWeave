"""固定されたテーブル契約から型付きAPI、操作SQL、呼出しを決定的に生成する。"""

import argparse
import json
import re
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
API_ROOT = ROOT / "backend/src/app/apis/entities"
ENTITY_ROOT = ROOT / "backend/src/app/entities"
HEADER = "# generate_entity_apis.py による自動生成。直接編集しない。\n"
READ_ONLY = {
    "backup_artifact",
    "backup_restore_intent",
    "audit_event",
    "outbox_event",
    "recipe_search_document",
    "ingredient_total",
    "workspace_revision",
    "pantry_consumption",
}
APPEND_ONLY = {
    "user_recipe_event",
    "generation_result",
    "validation_result",
    "recipe_signature",
    "generation_stratum_metric",
}
IMMUTABLE = {
    "product_version",
    "product_component",
    "food_allergen",
    "product_allergen",
    "nutrition_fact",
    "form_yield",
    "scaling_rule",
    "scaling_point",
    "media_asset",
    "generation_policy",
    "compatibility_rule",
    "food_identity",
    "food_identity_member",
    "generation_template",
    "product_preparation_rule",
}
OWNER_PARENT = {
    "menu_item": "menu_id",
    "menu_ingredient_override": "menu_item_id",
    "cooking_session": "menu_id",
    "session_task": "session_id",
    "task_dependency": "before_task_id",
    "resource_reservation": "task_id",
    "ingredient_total": "session_id",
    "shopping_item": "session_id",
    "receipt_line": "import_id",
}


def pascal(value: str) -> str:
    return "".join(part.title() for part in value.split("_"))


def load_tables() -> list[dict[str, Any]]:
    """取得済み正本の列型と語彙だけを入力とし、外部からテーブル名を受け取らない。"""
    source = json.loads((ROOT / "spec/database/source-sheet.json").read_text())["tabs"]
    enums: dict[str, list[str]] = defaultdict(list)
    for row in source["03_enum全値"][1:]:
        enums[row[0]].append(row[1])
    enums["generation_shard_state"] = ["queued", "running", "done", "failed"]
    enums["candidate_state"] = [
        "pending",
        "invalid",
        "generated",
        "duplicate",
        "accepted",
        "failed",
    ]
    metadata = json.loads((ROOT / "database/schema_catalog.json").read_text())
    tables = [table for table in metadata["tables"] if table["retention"] != "legacy"]
    for table in tables:
        table["rule"] = table.get("source_rules", "業務APIとDB制約に従う")
        references = {
            fk["columns"][0]: fk["referenced_table"] + "." + fk["referenced_columns"][0]
            for fk in table["foreign_keys"]
            if len(fk["columns"]) == 1
        }
        for col in table["columns"]:
            col["reference"] = references.get(col["name"])
    original = {row[2] for row in source["01_テーブル一覧"][1:]}
    if not original <= {table["name"] for table in tables}:
        raise ValueError("正本テーブル集合が実装にありません")
    return tables


def scope(
    table: dict[str, Any], tables: dict[str, dict[str, Any]], alias: str = "t", level: int = 0
) -> str:
    """本人所有者への固定FK経路をSQL述語へ変換する。"""
    name = table["name"]
    if name == "app_user":
        return f"{alias}.id = %(actor_id)s"
    if any(col["name"] == "user_id" for col in table["columns"]):
        return f"{alias}.user_id = %(actor_id)s"
    if name in OWNER_PARENT:
        column = next(col for col in table["columns"] if col["name"] == OWNER_PARENT[name])
        parent = str(column["reference"]).split(".")[0]
        next_alias = f"owner_{level}"
        condition = scope(tables[parent], tables, next_alias, level + 1)
        return (
            f"EXISTS (\n    SELECT {next_alias}.id\n"
            f"    FROM recipeweave.{parent} AS {next_alias}\n"
            f"    WHERE {next_alias}.id = {alias}.{column['name']}\n"
            f"        AND {condition}\n)"
        )
    return "TRUE"


def actions(table: dict[str, Any]) -> tuple[str, ...]:
    """保持方針に沿い、監査・派生・公開済み版へ汎用削除を公開しない。"""
    name = table["name"]
    result = ["list", "get"]
    if name in READ_ONLY:
        return tuple(result)
    if name != "app_user":
        result.append("create")
    if name not in IMMUTABLE | APPEND_ONLY | {"generation_shard"}:
        result.append("update")
    if table["retention"] == "owned" and name != "app_user":
        result.append("delete")
    return tuple(result)


def python_type(column: dict[str, Any]) -> str:
    kind = column["type"]
    if column["enum"]:
        result = "Literal[" + ", ".join(repr(value) for value in column["enum"]) + "]"
    elif kind == "uuid":
        result = "UUID"
    elif kind == "uuid[]":
        result = "list[UUID]"
    elif kind == "timestamptz":
        result = "AwareDatetime"
    elif kind == "date":
        result = "date"
    elif kind == "boolean":
        result = "bool"
    elif kind == "integer":
        result = "int"
    elif kind == "bigint":
        result = "BigInteger"
    elif kind.startswith("numeric"):
        result = "Decimal"
    elif kind == "jsonb":
        key = column.get("table", "") + "." + column["name"]
        if key not in JSON_TYPES:
            raise ValueError(f"JSON列の具体契約が未定義です: {key}")
        result = JSON_TYPES[key]
    elif kind.startswith("vector("):
        result = "list[float]"
    else:
        result = "str"
    if column["nullable"]:
        result += " | None"
    return result


JSON_TYPES = {
    "operation_parameter.allowed_values": "list[str]",
    "generation_policy.parameter_json": "GenerationParameters",
    "generation_result.input_snapshot": "GenerationInput",
    "compatibility_rule.predicate": "Predicate",
    "media_asset.parameter_contract": "MediaParameters",
    "validation_result.evidence": "ValidationEvidence",
    "cooking_session.input_snapshot": "CookingInput",
    "recipe_signature.canonical_payload": "CanonicalRecipe",
    "outbox_event.payload": "OutboxPayload",
    "product_preparation_rule.parameter_contract": "ProductPreparation",
    "generation_template.contract": "GenerationTemplateContract",
}


def field_line(column: dict[str, Any], optional_default: bool = False) -> str:
    options = ["description=" + repr(column["description"])]
    if column["type"].startswith("numeric"):
        options += ["max_digits=20", "decimal_places=6", "allow_inf_nan=False"]
    for check in [] if column["type"] == "bigint" else column.get("checks", []):
        match = re.fullmatch(
            re.escape(column["name"]) + r" (>=|<=|>|<) (-?[0-9]+(?:\.[0-9]+)?)", check
        )
        if match:
            options.append(
                {">": "gt", ">=": "ge", "<": "lt", "<=": "le"}[match[1]] + "=" + match[2]
            )
    if column["type"].startswith("char("):
        length = int(column["type"][5:-1])
        options += [f"min_length={length}", f"max_length={length}"]
    if column["type"] == "text" and not column["enum"]:
        maximum = min(20000, column.get("max_length", 20000))
        options += ["min_length=1", f"max_length={maximum}"]
    if column["type"] == "vector(768)":
        options += ["min_length=768", "max_length=768"]
    if column["type"] == "uuid[]":
        options += ["max_length=1024"]
    if optional_default and column["nullable"]:
        options.insert(0, "default=None")
    return f"    {column['name']}: {python_type(column)} = Field({', '.join(options)})\n"


def models_output(tables: list[dict[str, Any]]) -> str:
    chunks = [
        HEADER,
        '''from datetime import date
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, JsonValue

from app.entities.json_contracts import (
    BigInteger, CanonicalRecipe, CookingInput, GenerationInput, GenerationParameters,
    GenerationTemplateContract, MediaParameters, OutboxPayload, Predicate,
    ProductPreparation, ValidationEvidence,
)


class EntityModel(BaseModel):
    """追加項目を拒否し、行ごとの列契約をOpenAPIへ公開する。"""

    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

''',
    ]
    for table in tables:
        name = table["name"]
        for col in table["columns"]:
            col["table"] = name
        prefix = pascal(name)
        chunks += [
            f"\nclass {prefix}Row(EntityModel):\n",
            f'    """{table["description"]}のDB応答。"""\n\n',
        ]
        chunks += [field_line(col) for col in table["columns"]]
        chunks += [
            '    etag: str = Field(pattern=r"^[0-9]+$", '
            'description="更新・削除時のIf-Matchに使う行版")\n'
        ]
        columns = editable_columns(table)
        chunks += [
            f"\n\nclass {prefix}Write(EntityModel):\n",
            f'    """{table["description"]}の編集可能列。未指定NULL列はNULLにする。"""\n\n',
        ]
        chunks += [field_line(col, optional_default=True) for col in columns]
    return "".join(chunks)


def identifier(name: str) -> str:
    return '"offset"' if name == "offset" else name


def editable_columns(table: dict[str, Any]) -> list[dict[str, Any]]:
    """所有者の根と競合判定用の版はサーバーだけが管理する。"""
    excluded = {"id", "created_at", "owner_id"}
    excluded.update(
        {"app_user": {"auth_subject", "state"}, "menu": {"revision"}}.get(table["name"], set())
    )
    return [col for col in table["columns"] if col["name"] not in excluded]


def query_text(table: dict[str, Any], action: str, tables: dict[str, dict[str, Any]]) -> str:
    name = table["name"]
    all_columns = ",\n    ".join(f"t.{identifier(col['name'])}" for col in table["columns"])
    projection = all_columns + ",\n    t.xmin::text AS etag"
    owner = scope(table, tables)
    label = dict(
        list="一覧取得", get="取得", create="作成", update="条件付き更新", delete="条件付き削除"
    )
    comment = f"-- {table['description']}を{label[action]}する。\n"
    comment += "-- 値は名前付きパラメータで束縛する。\n"
    if action == "list":
        return (
            comment
            + f"SELECT\n    {projection}\nFROM recipeweave.{name} AS t\nWHERE {owner}\n"
            + "    AND (%(after_id)s::uuid IS NULL OR t.id > %(after_id)s)\n"
            + "ORDER BY t.id\nLIMIT %(page_limit)s;\n"
        )
    if action == "get":
        return (
            comment
            + f"SELECT\n    {projection}\nFROM recipeweave.{name} AS t\n"
            + f"WHERE t.id = %(row_id)s\n    AND {owner};\n"
        )
    columns = [col["name"] for col in editable_columns(table)]
    if action == "create":
        insert_columns = ",\n    ".join(identifier(col) for col in ["id"] + columns)
        params = ",\n    ".join(["%(row_id)s"] + [f"%({col})s" for col in columns])
        if name == "menu":
            insert_columns += ",\n    revision"
            params += ",\n    1"
        if name == "recipe_embedding":
            params = params.replace("%(embedding)s", "%(embedding)s::vector")
        return (
            comment
            + f"INSERT INTO recipeweave.{name} AS t (\n    {insert_columns}\n)\n"
            + f"VALUES (\n    {params}\n)\nRETURNING\n    {projection};\n"
        )
    where = f"t.id = %(row_id)s\n    AND t.xmin::text = %(expected_etag)s\n    AND {owner}"
    if action == "update":
        assigns = ",\n    ".join(f"{identifier(column)} = %({column})s" for column in columns)
        if name == "menu":
            assigns += ",\n    revision = t.revision + 1"
        if name == "recipe_embedding":
            assigns = assigns.replace("%(embedding)s", "%(embedding)s::vector")
        return (
            comment
            + f"UPDATE recipeweave.{name} AS t\nSET\n    {assigns}\nWHERE {where}\n"
            + f"RETURNING\n    {projection};\n"
        )
    return (
        comment
        + f"DELETE FROM recipeweave.{name} AS t\nWHERE {where}\nRETURNING\n    {projection};\n"
    )


def wrapper(sql: str, function: str = "execute", table: dict[str, Any] | None = None) -> str:
    """値の集合をSQLから宣言し、列挙したパラメータ以外はドライバへ渡さない。"""
    names = sorted(set(re.findall(r"%\((\w+)\)s", sql)))
    types = {
        "row_id": "UUID",
        "actor_id": "UUID",
        "reference_id": "UUID",
        "after_id": "UUID | None",
        "page_limit": "int",
        "expected_etag": "str",
        "preview": "bool",
    }
    if table is not None:
        for column in table["columns"]:
            kind = column["type"]
            column_type = {
                "uuid": "UUID",
                "uuid[]": "list[UUID]",
                "boolean": "bool",
                "integer": "int",
                "bigint": "int",
                "date": "date",
                "timestamptz": "datetime",
                "jsonb": "Jsonb",
                "vector(768)": "list[float]",
            }.get(kind, "Decimal" if kind.startswith("numeric") else "str")
            types[column["name"]] = column_type + (" | None" if column["nullable"] else "")
    fields = "\n".join(f"    {name}: {types.get(name, 'str')}" for name in names)
    values_literal = ", ".join(f"{name!r}: values[{name!r}]" for name in names)
    return (
        HEADER
        + f'''from collections.abc import Mapping
from typing import Any, TypedDict
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from psycopg import Connection
from psycopg.types.json import Jsonb


class Parameters(TypedDict):
{fields}


SQL = """{sql}"""


def {function}(connection: Connection[dict[str, Any]],
               values: Mapping[str, Any]) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {{{values_literal}}}
    return list(connection.execute(SQL, params).fetchall())
'''
    )


def operation_files(
    table: dict[str, Any], action: str, tables: dict[str, dict[str, Any]]
) -> tuple[dict[Path, str], dict[str, Any]]:
    name = table["name"]
    key = f"{name}_{action}"
    directory = API_ROOT / key
    opid = "entity_" + key
    method = dict(list="GET", get="GET", create="POST", update="PUT", delete="DELETE")[action]
    path = f"/api/entities/{name}" + ("/{row_id}" if action in {"get", "update", "delete"} else "")
    description = (
        table["description"]
        + dict(list="の一覧", get="の取得", create="の作成", update="の更新", delete="の削除")[
            action
        ]
    )
    owned = scope(table, tables) != "TRUE"
    response = pascal(name) + "Row"
    request = pascal(name) + "Write"
    results = "list[" + response + "]" if action == "list" else response
    errors = [401, 403, 409, 422, 503]
    if action == "get":
        errors += [404]
    if action in {"update", "delete"}:
        errors += [428]
    errors.sort()
    files: dict[Path, str] = {}
    idempotency = "GETは副作用なし。POSTは新規IDを採番する。"
    if action in {"update", "delete"}:
        idempotency = "If-Matchによる同一行版の条件付き操作"
    effects = "読取りのみ"
    if action not in {"get", "list"}:
        effects = "正規化行の変更。監査を追記しカタログ変更はoutboxへ通知する。"
    files[directory / "contract.py"] = (
        HEADER
        + f"""from app.core.contracts import OperationContract

CONTRACT = OperationContract(
    operation_id={opid!r}, slug={("entities/" + key)!r}, method={method!r},
    path={path!r}, summary={description!r},
    authentication="bearer", errors={tuple(errors)!r},
    idempotency={idempotency!r},
    transaction="本人所有権・参照・DB制約・監査・outboxを同じトランザクションで検査する",
    effects={effects!r},
)
"""
    )
    router_args = ["identity: IdentityDependency", "database: DatabaseDependency"]
    function_args = ["service: EntityService"]
    call_args = ["EntityService(database, identity)"]
    exec_args = [f"SPECIFICATIONS[{opid!r}]"]
    imports = ["from fastapi import APIRouter, Response"]
    if action in {"get", "update", "delete"}:
        router_args.append("row_id: UUID")
        function_args.append("row_id: UUID")
        call_args.append("row_id")
        exec_args.append("row_id=row_id")
        imports += ["from uuid import UUID"]
    if action in {"create", "update"}:
        router_args.append(f"payload: {request}")
        function_args.append(f"payload: {request}")
        call_args.append("payload")
        exec_args.append('payload=payload.model_dump(mode="python", by_alias=True)')
    if action in {"update", "delete"}:
        imports += ["from typing import Annotated", "from fastapi import Header"]
        router_args.append('if_match: Annotated[str | None, Header(alias="If-Match")] = None')
        function_args.append("if_match: str | None = None")
        call_args.append("if_match")
        exec_args.append("if_match=if_match")
    if action == "list":
        imports += [
            "from typing import Annotated",
            "from uuid import UUID",
            "from fastapi import Query",
        ]
        router_args += [
            "limit: Annotated[int, Query(ge=1, le=100)] = 50",
            "after: UUID | None = None",
        ]
        function_args += ["limit: int = 50", "after: UUID | None = None"]
        call_args += ["limit", "after"]
        exec_args += ["limit=limit", "after=after"]
    if action != "list":
        router_args.insert(0, "response: Response")
    model_imports = [response] + ([request] if action in {"create", "update"} else [])
    imports += [
        "from app.core.db import DatabaseDependency",
        "from app.core.identity import IdentityDependency",
        "from app.core.entity_service import EntityService",
        f"from app.apis.entities.{key}.contract import CONTRACT",
        f"from app.apis.entities.{key}.functions import execute",
        f"from app.apis.entities.{key}.schemas import " + ", ".join(model_imports),
    ]
    error_labels = {
        401: "認証が必要",
        403: "操作・参照権限なし",
        404: "対象なし",
        409: "同時更新またはDB業務制約違反",
        422: "入力不正",
        428: "If-Matchが必要",
        503: "DB接続不可",
    }
    errorresponses = (
        "{"
        + ", ".join(f'{code}: {{"description": {error_labels[code]!r}}}' for code in errors)
        + "}"
    )
    body = f"    result = execute({', '.join(call_args)})\n"
    if action != "list":
        body += '    response.headers["ETag"] = f\'"{result.etag}"\'\n'
    body += "    return result\n"
    files[directory / "router.py"] = (
        HEADER
        + "\n".join(imports)
        + f'''\n
router = APIRouter(tags=["正規化データ: {table["description"]}"])


@router.{method.lower()}(CONTRACT.path, operation_id=CONTRACT.operation_id,
    summary=CONTRACT.summary, response_model={results}, responses={errorresponses},
    status_code={201 if action == "create" else 200})
def handle({", ".join(router_args)}) -> {results}:
    """{description}。認証情報は依存から取得し、本人所有または管理者権限を検査する。"""
{body}
'''
    )
    fn_imports = [
        "from app.core.entity_service import EntityService",
        "from app.entities.registry import SPECIFICATIONS",
        "from app.entities.models import " + ", ".join(model_imports),
    ]
    if action in {"get", "update", "delete", "list"}:
        fn_imports.insert(0, "from uuid import UUID")
    return_line = (
        f"    return [{response}.model_validate(row) for row in rows]"
        if action == "list"
        else f"    return {response}.model_validate(rows[0])"
    )
    files[directory / "functions.py"] = (
        HEADER
        + "\n".join(fn_imports)
        + f'''\n

def execute({", ".join(function_args)}) -> {results}:
    """{description}を固定操作契約で実行し、DB行を専用応答型へ検証する。"""
    rows = service.execute({", ".join(exec_args)})
{return_line}
'''
    )
    files[directory / "schemas.py"] = (
        HEADER
        + "from app.entities.models import "
        + ", ".join(f"{model} as {model}" for model in model_imports)
        + "\n"
    )
    files[directory / "samples.py"] = (
        HEADER
        + f'"""{description}。具体例は専用型と操作別受入テストに対応する。"""\n\n'
        + f"OPERATION_ID = {opid!r}\nTABLE = {name!r}\nACTION = {action!r}\n"
    )
    sql = query_text(table, action, tables)
    files[directory / f"sql/001_{action}.sql"] = sql
    files[directory / "generated/queries.py"] = wrapper(sql, table=table)
    refs = []
    if action in {"create", "update"}:
        for col in table["columns"]:
            if owned and col["reference"] == "recipe_version.id":
                refsql = """-- 新規書込みより前に料理版の公開条件または既存の本人履歴を検査する。
SELECT t.id
FROM recipeweave.recipe_version AS t
INNER JOIN recipeweave.recipe AS recipe ON t.recipe_id = recipe.id
WHERE t.id = %(reference_id)s
    AND (
        (t.status = 'published' AND t.validation = 'passed' AND recipe.status = 'published')
        OR (%(preview)s AND t.status = 'draft' AND recipe.status = 'draft')
        OR EXISTS (
            SELECT 1 FROM recipeweave.menu_item AS history_item
            INNER JOIN recipeweave.menu AS history_menu ON history_item.menu_id = history_menu.id
            WHERE history_menu.user_id = %(actor_id)s AND history_item.recipe_version_id = t.id
        )
        OR EXISTS (
            SELECT 1 FROM recipeweave.user_recipe_event AS history_event
            WHERE history_event.user_id = %(actor_id)s AND history_event.recipe_version_id = t.id
        )
    );
"""
                refkey = "reference_" + col["name"]
                files[directory / f"sql/{len(refs) + 2:03}_{refkey}.sql"] = refsql
                files[directory / f"generated/{refkey}.py"] = wrapper(refsql)
                refs.append((col["name"], refkey))
            elif (
                col["reference"] and scope(tables[col["reference"].split(".")[0]], tables) != "TRUE"
            ):
                parent = tables[col["reference"].split(".")[0]]
                refsql = f"-- 参照先の{parent['description']}が同じ利用者に属することを検証する。\n"
                refsql += f"SELECT t.id FROM recipeweave.{parent['name']} AS t\n"
                refsql += f"WHERE t.id = %(reference_id)s\n    AND {scope(parent, tables)};\n"
                refkey = "reference_" + col["name"]
                files[directory / f"sql/{len(refs) + 2:03}_{refkey}.sql"] = refsql
                files[directory / f"generated/{refkey}.py"] = wrapper(refsql)
                refs.append((col["name"], refkey))
    input_cols = (
        [col["name"] for col in editable_columns(table)] if action in {"create", "update"} else []
    )
    if name == "app_user":
        input_cols = [col for col in input_cols if col not in {"auth_subject", "state"}]
    return files, dict(
        operation_id=opid,
        key=key,
        table=name,
        action=action,
        owned=owned,
        input_columns=input_cols,
        json_columns=[col["name"] for col in table["columns"] if col["type"] == "jsonb"],
        bigint_columns=[col["name"] for col in table["columns"] if col["type"] == "bigint"],
        references=refs,
        immutable=name in IMMUTABLE,
    )


def render() -> dict[Path, str]:
    """生成領域だけの全出力をメモリー上で組み立てる。"""
    tables = load_tables()
    by_name = {table["name"]: table for table in tables}
    files = {ENTITY_ROOT / "models.py": models_output(tables)}
    operations = []
    for table in tables:
        for action in actions(table):
            generated, metadata = operation_files(table, action, by_name)
            files.update(generated)
            operations.append(metadata)
    registry = [HEADER, "from app.core.entity_contracts import OperationSpec\n"]
    for op in operations:
        registry += [
            f"from app.apis.entities.{op['key']}.generated.queries "
            f"import execute as {op['operation_id']}\n"
        ]
        for _, reference in op["references"]:
            registry += [
                f"from app.apis.entities.{op['key']}.generated.{reference} "
                f"import execute as {op['operation_id']}_{reference}\n"
            ]
    registry += ["\nSPECIFICATIONS: dict[str, OperationSpec] = {\n"]
    for op in operations:
        kwargs = ", ".join(
            f"{key}={tuple(op[key])!r}" if isinstance(op[key], list) else f"{key}={op[key]!r}"
            for key in [
                "operation_id",
                "table",
                "action",
                "owned",
                "input_columns",
                "json_columns",
                "bigint_columns",
                "immutable",
            ]
        )
        refs = ", ".join(f"({col!r}, {op['operation_id']}_{ref})" for col, ref in op["references"])
        registry += [
            f"    {op['operation_id']!r}: OperationSpec({kwargs}, query={op['operation_id']}, "
            f"reference_queries=({refs}{',' if refs else ''})),\n"
        ]
    registry += ["}\n"]
    files[ENTITY_ROOT / "registry.py"] = "".join(registry)
    routers = [
        HEADER,
        "from fastapi import FastAPI\n",
        "from app.entities.generation_routes import register_generation_routes\n",
    ]
    routers += [
        f"from app.apis.entities.{op['key']}.router import router as {op['operation_id']}\n"
        for op in operations
    ]
    routers += [
        "\n\ndef register_entity_routes(application: FastAPI) -> None:\n"
        '    """全テーブルの許可された固定ルートを登録する。"""\n'
    ]
    routers += [f"    application.include_router({op['operation_id']})\n" for op in operations]
    routers += ["    register_generation_routes(application)\n"]
    files[ENTITY_ROOT / "routes.py"] = "".join(routers)
    files[ENTITY_ROOT / "operation_inventory.json"] = (
        json.dumps(
            dict(
                schemaVersion=1,
                tables=[
                    dict(
                        name=t["name"], retention=t["retention"], actions=actions(t), rule=t["rule"]
                    )
                    for t in tables
                ],
                operations=operations,
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    for sqlpath, function in [
        ("audit", "append_audit"),
        ("outbox", "append_outbox"),
        ("workspace", "increment_workspace"),
    ]:
        text = (ROOT / f"backend/src/app/entities/sql/{sqlpath}.sql").read_text()
        files[ENTITY_ROOT / f"{sqlpath}_query.py"] = wrapper(text, function)
    files[ENTITY_ROOT / "audit_queries.py"] = (
        HEADER
        + "from app.entities.audit_query import append_audit as append_audit\n"
        + "from app.entities.outbox_query import append_outbox as append_outbox\n"
    )
    sql_formatter = shutil.which("sqlfluff")
    if sql_formatter is None:
        raise RuntimeError("固定したSQLFluffをPATHへ設定してください")
    with TemporaryDirectory(prefix="entity-sql-format-") as scratch:
        temporary_root = Path(scratch)
        sqlfiles = {
            path: temporary_root / path.relative_to(ROOT) for path in files if path.suffix == ".sql"
        }
        for path, target in sqlfiles.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(files[path])
        result = subprocess.run(
            [
                sql_formatter,
                "fix",
                "--force",
                "--config",
                str(ROOT / ".sqlfluff"),
                "--processes",
                "4",
                "--disable-progress-bar",
                str(temporary_root),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            lint_result = subprocess.run(
                [
                    sql_formatter,
                    "lint",
                    "--config",
                    str(ROOT / ".sqlfluff"),
                    "--processes",
                    "4",
                    "--disable-progress-bar",
                    "--format",
                    "json",
                    str(temporary_root),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            if lint_result.returncode:
                Path("/tmp/entity-sql-lint.json").write_text(lint_result.stdout)
                raise RuntimeError("SQL解析・整形失敗。/tmp/entity-sql-lint.jsonを確認してください")
        for path, target in sqlfiles.items():
            files[path] = target.read_text()
            stem = "queries" if path.stem.startswith("001_") else path.stem[4:]
            files[path.parent.parent / f"generated/{stem}.py"] = wrapper(
                files[path], table=by_name[path.parent.parent.name.rsplit("_", 1)[0]]
            )
    formatter = shutil.which("ruff")
    if formatter is None:
        raise RuntimeError("固定したRuffをPATHへ設定してください")
    with TemporaryDirectory(prefix="entity-api-format-") as scratch:
        temporary_root = Path(scratch)
        pyfiles = {
            path: temporary_root / path.relative_to(ROOT) for path in files if path.suffix == ".py"
        }
        for path, target in pyfiles.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                files[path]
                .replace("ノード", "節点")
                .translate(str.maketrans({"（": "(", "）": ")", "×": "x", "：": ":"}))
            )
        subprocess.run(
            [
                formatter,
                "check",
                "--config",
                str(ROOT / "backend/pyproject.toml"),
                "--config",
                'lint.isort.known-first-party=["app"]',
                "--fix",
                "--unsafe-fixes",
                str(temporary_root),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        subprocess.run(
            [
                formatter,
                "format",
                "--config",
                str(ROOT / "backend/pyproject.toml"),
                str(temporary_root),
            ],
            text=True,
            capture_output=True,
            check=True,
        )
        for path, target in pyfiles.items():
            files[path] = target.read_text()
    return files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    files = render()
    stale = []
    managed = set(API_ROOT.rglob("*.py")) | set(API_ROOT.rglob("*.sql"))
    for path in managed - set(files):
        if args.check:
            stale.append(str(path.relative_to(ROOT)))
        else:
            path.unlink()
    for path, text in files.items():
        if path.is_symlink() or any(
            parent.is_symlink() for parent in path.parents if parent != ROOT
        ):
            raise ValueError(f"シンボリックリンクの出力を拒否します: {path}")
        if not path.is_file() or path.read_text() != text:
            if args.check:
                stale.append(str(path.relative_to(ROOT)))
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                temporary = path.with_suffix(path.suffix + ".tmp")
                temporary.write_text(text)
                temporary.replace(path)
    if stale:
        print("Entity API drift: " + ", ".join(stale))
        return 1
    print(f"Entity API生成済み: {len(files)}ファイル")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
