"""実FastAPIのOpenAPIと操作メタデータからAPI仕様を生成する。"""

import ast
import importlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .common import DesignError, document, read_source, table
from .database import Query, Table
from .details import render_detail, render_messages
from .flow import render_sequences
from .test_contracts import factor_section

METHODS = {"get", "post", "put", "patch", "delete", "options", "head"}


@dataclass
class Operation:
    id: str
    slug: str
    method: str
    path: str
    spec: dict[str, Any]
    contract: dict[str, Any]
    directory: Path


def dereference(node: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    if "$ref" not in node:
        return node
    reference = node["$ref"]
    if not reference.startswith("#/"):
        raise DesignError(f"外部OpenAPI参照は未対応です: {reference}")
    value: Any = spec
    for part in reference[2:].split("/"):
        key = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or key not in value:
            raise DesignError(f"OpenAPI参照が解決できません: {reference}")
        value = value[key]
    if not isinstance(value, dict):
        raise DesignError(f"オブジェクト以外へのOpenAPI参照です: {reference}")
    return value | {key: value for key, value in node.items() if key != "$ref"}


def validate_references(value: Any, spec: dict[str, Any]) -> None:
    if isinstance(value, dict):
        if "$ref" in value:
            dereference(value, spec)
        for child in value.values():
            validate_references(child, spec)
    elif isinstance(value, list):
        for child in value:
            validate_references(child, spec)


def load_operations(root: Path, spec: dict[str, Any]) -> list[Operation]:
    validate_references(spec, spec)
    contracts = {}
    for path in sorted((root / "backend/src/app/apis").glob("*/*/contract.py")):
        relative = path.parent.relative_to(root / "backend/src/app/apis")
        module_name = "app.apis." + ".".join(relative.parts) + ".contract"
        contract = asdict(importlib.import_module(module_name).CONTRACT)
        if contract["slug"] != str(relative):
            raise DesignError(f"APIのslugと配置先が一致しません: {path}")
        key = (contract["method"].upper(), contract["path"])
        if key in contracts:
            raise DesignError(f"APIメタデータが重複しています: {key}")
        contracts[key] = (contract, path.parent)
    operations = []
    ids = set()
    for route, path_spec in sorted(spec["paths"].items()):
        for method, item in sorted(path_spec.items()):
            if method not in METHODS:
                continue
            key = (method.upper(), route)
            if key not in contracts:
                raise DesignError(f"APIに操作メタデータがありません: {key}")
            contract, directory = contracts.pop(key)
            operation_id = item.get("operationId")
            if operation_id != contract["operation_id"] or operation_id in ids:
                raise DesignError(f"operationIdが不一致または重複しています: {key}")
            ids.add(operation_id)
            if item.get("summary") != contract["summary"]:
                raise DesignError(f"APIの要約とmetadataが一致しません: {key}")
            actual_errors = {
                int(status)
                for status in item["responses"]
                if status.isdigit() and int(status) >= 400
            }
            if actual_errors != set(contract["errors"]):
                raise DesignError(f"APIエラー定義とmetadataが一致しません: {key}")
            parameters = {}
            for parameter in path_spec.get("parameters", []) + item.get("parameters", []):
                resolved = dereference(parameter, spec)
                parameters[(resolved["in"], resolved["name"])] = resolved
            path_parameters = {p["name"] for p in parameters.values() if p["in"] == "path"}
            if path_parameters != set(re.findall(r"\{([^}]+)\}", route)) or any(
                not p.get("required") for p in parameters.values() if p["in"] == "path"
            ):
                raise DesignError(f"パス変数とパラメーター定義が一致しません: {key}")
            security = item.get("security", spec.get("security", []))
            public = contract["authentication"].startswith("public")
            if public != (not security or {} in security):
                raise DesignError(f"OpenAPIと認証メタデータが一致しません: {key}")
            merged = dict(item)
            merged["parameters"] = list(parameters.values())
            operations.append(
                Operation(
                    operation_id,
                    contract["slug"],
                    method.upper(),
                    route,
                    merged,
                    contract,
                    directory,
                )
            )
    if contracts:
        raise DesignError(f"実ルートに存在しない操作メタデータ: {sorted(contracts)}")
    return operations


def standalone_openapi(op: Operation, spec: dict[str, Any]) -> dict[str, Any]:
    """この操作から到達する参照だけを閉包し、単独で読めるOpenAPIを作る。"""
    components: dict[str, Any] = {}
    seen: set[str] = set()

    def collect(value: Any) -> None:
        if isinstance(value, dict):
            reference = value.get("$ref")
            if reference and reference not in seen:
                seen.add(reference)
                parts = reference.split("/")
                if len(parts) != 4 or parts[:2] != ["#", "components"]:
                    raise DesignError(f"操作単位でのOpenAPI参照に未対応です: {reference}")
                resolved = dereference({"$ref": reference}, spec)
                components.setdefault(parts[2], {})[parts[3]] = resolved
                collect(resolved)
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    collect(op.spec)
    security = op.spec.get("security", spec.get("security", []))
    for requirement in security:
        for name in requirement:
            scheme = spec.get("components", {}).get("securitySchemes", {}).get(name)
            if scheme is None:
                raise DesignError(f"認証schemeが未定義です: {name}")
            components.setdefault("securitySchemes", {})[name] = scheme
    result = {
        "openapi": spec["openapi"],
        "info": spec["info"],
        "paths": {op.path: {op.method.lower(): op.spec}},
        "components": components,
    }
    if "servers" in spec:
        result["servers"] = spec["servers"]
    return result


def schema_type(schema: dict[str, Any]) -> str:
    if "$ref" in schema:
        return schema["$ref"].rsplit("/", 1)[-1]
    for join in ("anyOf", "oneOf", "allOf"):
        if join in schema:
            return join + "(" + ", ".join(schema_type(s) for s in schema[join]) + ")"
    kind = schema.get("type", "任意のJSON")
    if kind == "array":
        return "array<" + schema_type(schema.get("items", {})) + ">"
    return str(kind) + (f" ({schema['format']})" if "format" in schema else "")


def restrictions(schema: dict[str, Any]) -> str:
    keys = (
        "enum",
        "const",
        "default",
        "minimum",
        "maximum",
        "exclusiveMinimum",
        "exclusiveMaximum",
        "minLength",
        "maxLength",
        "pattern",
        "minItems",
        "maxItems",
        "uniqueItems",
        "additionalProperties",
        "readOnly",
        "writeOnly",
    )
    values = [
        f"{key}={json.dumps(schema[key], ensure_ascii=False)}" for key in keys if key in schema
    ]
    for branch in ("anyOf", "oneOf", "allOf"):
        children = [
            f"{schema_type(child)}: {restrictions(child)}"
            for child in schema.get(branch, [])
            if restrictions(child) != "追加制約なし"
        ]
        if children:
            values.append(f"{branch}の制約=" + " / ".join(children))
    if "items" in schema:
        item_rules = restrictions(schema["items"])
        if item_rules != "追加制約なし":
            values.append("要素の制約=" + item_rules)
    return "; ".join(values) or "追加制約なし"


def schema_rows(schema: dict[str, Any], spec: dict[str, Any]) -> list[list[object]]:
    resolved = dereference(schema, spec)
    required = resolved.get("required", [])
    rows = []
    for name, field in resolved.get("properties", {}).items():
        rows.append(
            [
                name,
                schema_type(field),
                "必須" if name in required else "任意",
                restrictions(field),
                field.get("description", field.get("title", "")),
            ]
        )
    if not rows:
        rows.append(
            [
                "値全体",
                schema_type(schema),
                "—",
                restrictions(resolved),
                resolved.get("description", ""),
            ]
        )
    return rows


def render_interface(op: Operation, spec: dict[str, Any]) -> str:
    parameters = [
        [
            p["in"],
            p["name"],
            "必須" if p.get("required") else "任意",
            schema_type(p.get("schema", {})),
            restrictions(p.get("schema", {})),
            p.get("description", ""),
        ]
        for p in op.spec.get("parameters", [])
    ]
    request = []
    if "requestBody" in op.spec:
        body = dereference(op.spec["requestBody"], spec)
        request += ["必須" if body.get("required") else "省略可"]
        for media, value in body.get("content", {}).items():
            request += [
                f"### {media}",
                table(
                    ["項目", "型", "必須性", "制約", "説明"],
                    schema_rows(value.get("schema", {}), spec),
                ),
            ]
    else:
        request.append("リクエスト本文の定義なし。")
    responses = []
    for code, value in sorted(op.spec["responses"].items()):
        response = dereference(value, spec)
        responses.append(f"### HTTP {code}: {response.get('description', '')}")
        for media, content in response.get("content", {}).items():
            responses += [
                f"Content-Type: `{media}`",
                schema_type(content.get("schema", {})),
                table(
                    ["項目", "型", "必須性", "制約", "説明"],
                    schema_rows(content.get("schema", {}), spec),
                ),
            ]
        if "content" not in response:
            responses.append("OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。")
        if response.get("headers"):
            responses.append(
                table(
                    ["ヘッダー", "定義"],
                    [
                        [k, json.dumps(v, ensure_ascii=False)]
                        for k, v in response["headers"].items()
                    ],
                )
            )
    samples_path = op.directory / "samples.py"
    return document(
        f"インターフェース: {op.id}",
        [
            f"`{op.method} {op.path}` — {op.contract['summary']}",
            "## 認証\n\n"
            + json.dumps(op.spec.get("security", spec.get("security", [])), ensure_ascii=False)
            + "\n\n宣言: "
            + op.contract["authentication"],
            "## パラメーター\n\n"
            + (
                table(["場所", "名前", "必須性", "型", "制約", "説明"], parameters)
                if parameters
                else "なし。"
            ),
            "## リクエスト本文\n\n" + "\n\n".join(request),
            "## レスポンス\n\n" + "\n\n".join(responses),
            "## 操作のサンプル\n\n```python\n" + samples_path.read_text().rstrip() + "\n```",
            "[Swagger互換のOpenAPI JSON](interface.openapi.json)",
            "[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)",
            "## このAPIのOpenAPI定義\n\n```json\n"
            + json.dumps(op.spec, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n```",
        ],
    )


def test_sources(root: Path, operation: Operation) -> list[list[object]]:
    rows = []
    for path in sorted((root / "backend/tests").glob("test_*.py")):
        parsed = ast.parse(read_source(path, root))
        for node in ast.walk(parsed):
            if not isinstance(
                node, ast.FunctionDef | ast.AsyncFunctionDef
            ) or not node.name.startswith("test_"):
                continue
            # 明示的に対象URLを呼ぶテストだけを対応づけ、名前からの推測はしない。
            calls = [
                call
                for call in ast.walk(node)
                if isinstance(call, ast.Call)
                and isinstance(call.func, ast.Attribute)
                and call.func.attr == operation.method.lower()
                and call.args
                and isinstance(call.args[0], ast.Constant)
                and isinstance(call.args[0].value, str)
            ]
            prefix = operation.path.split("{")[0]
            if not any(
                call.args[0].value.split("?")[0] == operation.path
                or ("{" in operation.path and call.args[0].value.startswith(prefix))
                for call in calls
            ):
                continue
            assertions = [
                ast.unparse(item) for item in ast.walk(node) if isinstance(item, ast.Assert)
            ]
            rows.append(
                [
                    f"{path.relative_to(root)}::{node.name}",
                    ast.get_docstring(node) or "明示URLを呼び出すテスト",
                    " / ".join(assertions),
                ]
            )
    return rows


def render_api(
    root: Path,
    operations: list[Operation],
    spec: dict[str, Any],
    tables: dict[str, Table],
    queries: list[Query],
) -> dict[str, str]:
    outputs = {}
    outputs["api/README.md"] = document(
        "API一覧",
        [
            table(
                ["operationId", "HTTP", "パス", "要約", "認証", "応答"],
                [
                    [
                        f"[{op.id}](operations/{op.id}/interface.md)",
                        op.method,
                        op.path,
                        op.contract["summary"],
                        op.contract["authentication"],
                        ", ".join(sorted(op.spec["responses"])),
                    ]
                    for op in operations
                ],
            ),
            "[CRUD対応](CRUD.md) / [共有モデル](MODELS.md) / [共通エラー](ERRORS.md)",
        ],
    )
    crud_rows = []
    for name in sorted(tables):
        for op in operations:
            actions = set().union(
                *(q.actions.get(name, set()) for q in queries if q.operation == op.id)
            )
            if actions:
                crud_rows.append(
                    [
                        name,
                        f"[{op.id}](operations/{op.id}/detail.md)",
                        *("✓" if letter in actions else "—" for letter in "CRUD"),
                    ]
                )
    outputs["api/CRUD.md"] = document(
        "テーブルとAPIのCRUD対応",
        [
            "C=INSERT、R=SELECT、U=UPDATE、D=DELETE。SQL ASTから実対象を導出し、"
            "WHERE/RETURNINGを独立したRへ水増ししない。"
            "監査とアウトボックスの共有SQLも書込み操作に対応づける。",
            "数百APIを横一列へ並べず、表ごとに関連APIと4操作を縦に表示する。",
            table(["テーブル", "API", "C", "R", "U", "D"], crud_rows),
            "移行台帳等、APIから参照しない表の運用処理は個別テーブル仕様を参照する。",
        ],
    )
    models = []
    for name, schema in sorted(spec.get("components", {}).get("schemas", {}).items()):
        models += [
            f"## {name}",
            schema.get("description", ""),
            table(["項目", "型", "必須性", "制約", "説明"], schema_rows(schema, spec)),
            "```json\n"
            + json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True)
            + "\n```",
        ]
    outputs["api/MODELS.md"] = document("共有モデル・enum・制約", models)
    errors = []
    main_source = read_source(root / "backend/src/app/main.py", root)
    parsed = ast.parse(main_source)
    for node in parsed.body:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name.endswith(
            "_error"
        ):
            errors += [f"## {node.name}", "```python\n" + ast.unparse(node) + "\n```"]
    errors += [
        "## 本文サイズ制限",
        "```python\n"
        + read_source(root / "backend/src/app/core/middleware.py", root).rstrip()
        + "\n```",
    ]
    outputs["api/ERRORS.md"] = document(
        "共通エラー応答の実装仕様",
        [
            "実際の例外handlerと本文サイズ制限から生成する。OpenAPIにschemaがないエラーも実装で確認する。",
            *errors,
        ],
    )
    for op in operations:
        prefix = f"api/operations/{op.id}"
        owned = [q for q in queries if q.operation == op.id]
        outputs[f"{prefix}/interface.md"] = render_interface(op, spec)
        sequence, functions = render_sequences(op.directory, root, op.id)
        outputs[f"{prefix}/sequence.md"] = sequence
        outputs[f"{prefix}/queries.md"] = document(
            f"SQL仕様: {op.id}",
            [
                *(
                    f"## {q.source}\n\n"
                    + "実行条件: "
                    + q.condition
                    + "\n\n"
                    + table(
                        ["対象表", "CRUD", "参照・書込列"],
                        [
                            [name, ",".join(sorted(actions)), ", ".join(q.columns.get(name, []))]
                            for name, actions in sorted(q.actions.items())
                        ],
                    )
                    + "\n\nバインド変数: "
                    + (", ".join(q.parameters) or "なし")
                    + "\n\n```sql\n"
                    + q.sql.rstrip()
                    + "\n```"
                    for q in owned
                ),
                *(
                    []
                    if owned
                    else [
                        "このAPIはSQLを実行しない。データの取得元は下記関数・連携ポートを参照する。"
                    ]
                ),
                "SQLファイル→自動生成wrapper→連携adapter→functions→routerの境界で管理する。"
                "利用者入力はパラメーターとして渡し、SQL文字列へ連結しない。",
            ],
        )
        outputs[f"{prefix}/detail.md"] = render_detail(root, op, owned, tables, spec)
        outputs[f"{prefix}/messages.md"] = render_messages(root, op)
        operation_spec = standalone_openapi(op, spec)
        outputs[f"{prefix}/interface.openapi.json"] = (
            json.dumps(operation_spec, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        )
        tests = test_sources(root, op)
        outputs[f"{prefix}/tests.md"] = document(
            f"要因別単体テスト仕様: {op.id}",
            [
                factor_section(root, op),
                "次の一覧は対象HTTPメソッドとURLを明示的に呼ぶテストの静的抽出。"
                "テスト成功や全要件の受入完了を意味しない。間接fixture経由の対応を名前だけで推定しない。",
                table(["テストnode", "説明", "表明"], tests)
                if tests
                else "対象URLを直接呼ぶテストなし。間接的な検証は検証記録を参照する。",
                "宣言応答: " + ", ".join(sorted(op.spec["responses"])),
            ],
        )
    navigation = " / ".join(
        f"[{label}]({name}.md)"
        for name, label in [
            ("detail", "詳細"),
            ("interface", "入出力"),
            ("messages", "ログ"),
            ("queries", "SQL"),
            ("sequence", "シーケンス"),
            ("tests", "要因別試験"),
        ]
    )
    for name, content in list(outputs.items()):
        if name.startswith("api/operations/") and name.endswith(".md"):
            heading, separator, body = content.partition("\n\n")
            outputs[name] = (
                heading + separator + navigation + " / [API一覧](../../README.md)\n\n" + body
            )
    return outputs
