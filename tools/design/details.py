"""入力、SQL、共有サービスの実装から処理仕様と実ログを投影する。"""

import ast
from pathlib import Path
from typing import Any

from sqlglot import exp

from .common import DesignError, document, read_source, table
from .database import Query, Table, parse_one


def source_functions(
    path: Path, root: Path
) -> list[tuple[str, ast.FunctionDef | ast.AsyncFunctionDef]]:
    tree = ast.parse(read_source(path, root))
    functions = []
    for item in tree.body:
        if isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef):
            functions.append((item.name, item))
        elif isinstance(item, ast.ClassDef):
            functions.extend(
                (f"{item.name}.{fn.name}", fn)
                for fn in item.body
                if isinstance(fn, ast.FunctionDef | ast.AsyncFunctionDef)
            )
    return functions


def operation_sources(root: Path, op: Any) -> list[Path]:
    paths = [op.directory / "router.py", op.directory / "functions.py"]
    if op.slug.startswith("entities/"):
        paths += [root / "backend/src/app/core/entity_service.py"]
    if op.slug.startswith("workspace/"):
        paths += [root / "backend/src/app/core/workspace_service.py"]
        if "cooking_session" in op.slug:
            paths += [root / "backend/src/app/core/cooking_service.py"]
        if op.slug == "workspace/preview_cooking_plan":
            paths += [
                root / "backend/src/app/core/cooking_plan_service.py",
                root / "backend/src/app/integrations/catalog/postgres_provider.py",
            ]
    if op.slug.startswith("generation/"):
        paths += [
            root / "backend/src/app/core/entity_generation.py",
            root / "backend/src/app/core/entity_service.py",
        ]
    if op.slug.startswith("backup/"):
        paths += [root / "backend/src/app/core/backup_service.py"]
        if op.slug == "backup/restore_backup":
            paths += [root / "backend/src/app/core/workspace_service.py"]
    if op.slug.startswith(("foods/", "recipes/")):
        paths += [root / "backend/src/app/integrations/catalog/postgres_provider.py"]
    return paths


def selected_functions(
    root: Path, op: Any, path: Path
) -> list[tuple[str, ast.FunctionDef | ast.AsyncFunctionDef]]:
    functions = source_functions(path, root)
    if path.parent == op.directory:
        return functions
    caller = ast.parse(read_source(op.directory / "functions.py", root))
    by_name = {name.rsplit(".", 1)[-1]: (name, fn) for name, fn in functions}
    calls = list(ast.walk(caller))
    if path.name == "entity_service.py" and op.directory.parent.name == "generation":
        calls += list(
            ast.walk(
                ast.parse(read_source(root / "backend/src/app/core/entity_generation.py", root))
            )
        )
    if path.name == "cooking_service.py":
        workspace = root / "backend/src/app/core/workspace_service.py"
        methods = selected_functions(root, op, workspace)
        calls += [node for _, fn in methods for node in ast.walk(fn)]
    if path.name == "workspace_service.py" and op.directory.parent.name == "backup":
        backup = root / "backend/src/app/core/backup_service.py"
        methods = selected_functions(root, op, backup)
        calls += [node for _, fn in methods for node in ast.walk(fn)]
    if path.name == "postgres_provider.py" and op.directory.name == "preview_cooking_plan":
        plan_service = root / "backend/src/app/core/cooking_plan_service.py"
        methods = selected_functions(root, op, plan_service)
        calls += [node for _, fn in methods for node in ast.walk(fn)]
    wanted = set()
    for node in calls:
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id in by_name:
            wanted.add(node.func.id)
        elif (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id in {"service", "catalog"}
            and node.func.attr in by_name
        ):
            wanted.add(node.func.attr)
        elif (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Name)
            and node.func.value.func.id in {"CookingService", "WorkspaceService"}
        ):
            wanted.add(node.func.attr)
    found = set()
    while wanted - found:
        name = sorted(wanted - found)[0]
        found.add(name)
        if name not in by_name:
            raise DesignError(f"共有サービスの関数が解決できません: {path}:{name}")
        fn = by_name[name][1]
        for node in ast.walk(fn):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in by_name:
                wanted.add(node.func.id)
            elif (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "self"
            ):
                wanted.add(node.func.attr)
    return [(name, fn) for name, fn in functions if name.rsplit(".", 1)[-1] in found]


def expression_origins(root: Path, op: Any, extra: Path | None = None) -> dict[str, str]:
    """辞書値の代入式を残し、パラメーター名から入力元を推測しない。"""
    result = {}
    paths = [extra] if extra is not None else operation_sources(root, op)
    for path in paths:
        functions = (
            source_functions(path, root)
            if extra is not None
            else selected_functions(root, op, path)
        )
        for item in (node for _, fn in functions for node in ast.walk(fn)):
            if isinstance(item, ast.Dict):
                for key, value in zip(item.keys, item.values, strict=True):
                    if isinstance(key, ast.Constant) and isinstance(key.value, str):
                        result.setdefault(key.value, []).append(
                            f"{ast.unparse(value)} ({path.relative_to(root)}:{value.lineno})"
                        )
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Subscript) and isinstance(target.slice, ast.Constant):
                        result.setdefault(str(target.slice.value), []).append(
                            f"{ast.unparse(item.value)} ({path.relative_to(root)}:{item.lineno})"
                        )
            if isinstance(item, ast.Call):
                for keyword in item.keywords:
                    if keyword.arg:
                        result.setdefault(keyword.arg, []).append(
                            f"{ast.unparse(keyword.value)} ({path.relative_to(root)}:{item.lineno})"
                        )
    return {name: " / ".join(dict.fromkeys(values)) for name, values in result.items()}


def backup_row_origins(root: Path, op: Any) -> dict[str, dict[str, str]]:
    """復元行の展開を追跡し、新規発行ID等の同名引数と混同しない。"""
    if op.slug not in {"backup/preview_backup", "backup/restore_backup"}:
        return {}
    service_path = root / "backend/src/app/core/backup_service.py"
    functions = dict(source_functions(service_path, root))
    reference = functions.get("BackupService.check_references")
    replace = functions.get("BackupService.replace_rows")
    if reference is None or replace is None:
        raise DesignError("バックアップ行の検証・全置換の実装を解決できません")
    expressions = {ast.unparse(item) for item in ast.walk(reference)}
    replacements = {ast.unparse(item) for item in ast.walk(replace)}
    if (
        not {
            "document.tables.model_dump(mode='python')",
        }
        <= expressions
        or not {
            "values = dict(row)",
            "queries.run('q200_insert_' + table, **values)",
            "Jsonb(to_jsonable_python(values[column]))",
            "int(values[column])",
        }
        <= replacements
    ):
        raise DesignError("バックアップ行からSQL引数への代入経路が変わりました")
    inventory_path = root / "backend/src/app/backup/inventory.py"
    inventory = ast.parse(read_source(inventory_path, root))
    definitions = [
        item.value
        for item in inventory.body
        if isinstance(item, ast.AnnAssign)
        and isinstance(item.target, ast.Name)
        and item.target.id == "TABLES"
    ]
    if len(definitions) != 1:
        raise DesignError("バックアップ対象列の実装定義を一意に解決できません")
    metadata = ast.literal_eval(definitions[0])
    result = {}
    for name, item in metadata.items():
        columns = {}
        for column in item["columns"]:
            conversion = "値を維持"
            if column in item["json_columns"]:
                conversion = "非NULLならJsonb(to_jsonable_python(values[column]))へ変換"
            elif column in item["bigint_columns"]:
                conversion = "非NULLならint(values[column])へ変換"
            columns[column] = (
                f"request.backup.tables.{name} の各行.{column} → "
                "document.tables.model_dump(mode='python') → data[table] → dict(row) → "
                f"{conversion} → **valuesの名前付きSQL引数。"
                f"({service_path.relative_to(root)}:{reference.lineno}, {replace.lineno})"
            )
        result[name] = columns
    return result


def render_detail(
    root: Path, op: Any, queries: list[Query], tables: dict[str, Table], spec: dict[str, Any]
) -> str:
    from .api import schema_rows, schema_type

    sections = [
        f"`{op.method} {op.path}` — {op.contract['summary']}",
        "## 入力と処理前提",
        table(
            ["項目", "仕様"],
            [
                [key, op.contract[key]]
                for key in ("authentication", "idempotency", "transaction", "effects")
            ],
        ),
        table(
            ["入力場所", "名前", "型", "必須"],
            [
                [p["in"], p["name"], schema_type(p.get("schema", {})), p.get("required", False)]
                for p in op.spec.get("parameters", [])
            ],
        ),
    ]
    body = op.spec.get("requestBody", {})
    for media, content in body.get("content", {}).items():
        sections += [
            f"### 本文: {media}",
            table(
                ["入力", "型", "必須", "制約", "意味"], schema_rows(content.get("schema", {}), spec)
            ),
        ]
    origins = expression_origins(root, op)
    backup_origins = backup_row_origins(root, op)
    identity_path = root / "backend/src/app/core/identity.py"
    identity_origins = expression_origins(root, op, identity_path) if identity_path.exists() else {}
    sections += ["## データベースの対象と値の流れ"]
    for query in queries:
        if query.transaction_effect is not None:
            sections += [
                f"### `{query.source}`",
                "実行条件: " + query.condition,
                query.transaction_effect,
                "この文自体の行CRUDはない。制約違反は呼出元へ返し、"
                "プレビューの試験書込みを保持するか戻すかは呼出元のトランザクション制御に従う。",
            ]
            continue
        statement = parse_one(query.sql, query.source)
        sections += [
            f"### `{query.source}`",
            "実行条件: " + query.condition,
            table(
                ["物理テーブル", "操作", "対象列と意味"],
                [
                    [
                        name,
                        "".join(sorted(actions)),
                        "; ".join(
                            f"{c.name}: {c.description}"
                            for c in tables[name].columns
                            if c.name in query.columns.get(name, [])
                        ),
                    ]
                    for name, actions in sorted(query.actions.items())
                ],
            ),
        ]
        where = statement.args.get("where")
        sections.append(
            "対象条件: `"
            + (where.sql(dialect="postgres") if where else "SQL上の絞り込みなし")
            + "`"
        )
        for lock in statement.find_all(exp.Lock):
            sections.append("行ロック: `" + lock.sql(dialect="postgres") + "`")
        binds = []
        for parameter in query.parameters:
            query_origins = identity_origins if "/auth/get_me/sql/" in query.source else origins
            if backup_origins and Path(query.source).stem.startswith("q200_insert_"):
                target = Path(query.source).stem.removeprefix("q200_insert_")
                if query.actions != {f"recipeweave.{target}": {"C"}}:
                    raise DesignError(f"バックアップの挿入先と対象定義が不一致です: {query.source}")
                query_origins = backup_origins.get(target, {})
                if parameter not in query_origins:
                    raise DesignError(f"バックアップ列の値の出所がありません: {target}.{parameter}")
            source = query_origins.get(parameter)
            if (
                not source
                and op.slug.startswith("entities/")
                and "/auth/get_me/sql/" not in query.source
            ):
                source = (
                    "検証済みリクエストモデル → payload → values → params。"
                    "共有サービスがJSONB/整数列を変換する。"
                )
            binds.append([parameter, source or "型付きクエリの引数。呼出元のSQL仕様を参照。"])
        sections.append(table(["SQLバインド", "実装上の値の出所"], binds))
        changed = []
        if isinstance(statement, exp.Insert) and isinstance(statement.this, exp.Schema):
            values = statement.expression
            if isinstance(values, exp.Values):
                for row in values.expressions:
                    for column, value in zip(
                        statement.this.expressions, row.expressions, strict=True
                    ):
                        changed.append([column.name, value.sql(dialect="postgres")])
        elif isinstance(statement, exp.Update):
            changed = [
                [assignment.this.name, assignment.expression.sql(dialect="postgres")]
                for assignment in statement.expressions
            ]
        if changed:
            sections += [
                "変更する列とSQL式",
                table(["書込み列", "値・式（バインド元は上表）"], changed),
            ]
        conflict = statement.args.get("conflict")
        if conflict is not None:
            sections.append("競合時の処理: `" + conflict.sql(dialect="postgres") + "`")
            if conflict.expressions:
                sections.append(
                    table(
                        ["既存行の更新列", "競合時に設定する式"],
                        [
                            [assignment.this.name, assignment.expression.sql(dialect="postgres")]
                            for assignment in conflict.expressions
                        ],
                    )
                )
        if isinstance(statement, exp.Delete):
            sections.append(
                "上記の条件に一致する行を削除する。参照先への削除動作はテーブル仕様の外部キー定義に従う。"
            )
        if statement.args.get("expressions"):
            sections.append(
                "代入・選択式: `"
                + "; ".join(e.sql(dialect="postgres") for e in statement.expressions)
                + "`"
            )
    if not queries:
        sections.append(
            "この操作に属するSQLはない。永続化を行う処理は下記の関数責務と依存ポートで確認する。"
        )
    conditions, returns, responsibility = [], [], []
    for path in operation_sources(root, op):
        for name, fn in selected_functions(root, op, path):
            source = f"{path.relative_to(root)}:{fn.lineno}"
            responsibility.append([name, ast.get_docstring(fn) or "個別説明なし", source])
            for node in ast.walk(fn):
                if isinstance(node, ast.If):
                    rejected = [
                        ast.unparse(item.exc)
                        for child in node.body
                        for item in ast.walk(child)
                        if isinstance(item, ast.Raise) and item.exc
                    ]
                    if rejected:
                        conditions.append([ast.unparse(node.test), " / ".join(rejected), source])
                elif isinstance(node, ast.Return):
                    returns.append(
                        [name, ast.unparse(node.value) if node.value else "本文なし", source]
                    )
    sections += [
        "## 分岐・拒否条件",
        table(["判定条件", "例外・応答", "定義元"], conditions),
        "## 出力",
        table(["関数", "返却式", "定義元"], returns),
        "APIとして返す型・status・headerは [インターフェース](interface.md) の実OpenAPIを参照。",
        "## 責務",
        table(["関数", "処理", "定義元"], responsibility),
        "[SQL](queries.md) / [シーケンス](sequence.md) / [ログ](messages.md) / "
        "[要因別テスト](tests.md)",
    ]
    return document(f"詳細設計: {op.id}", sections)


def render_messages(root: Path, op: Any) -> str:
    rows = []
    levels = {"debug", "info", "warning", "error", "critical", "exception", "log"}
    for path in operation_sources(root, op):
        for name, fn in selected_functions(root, op, path):
            for node in ast.walk(fn):
                if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                    continue
                if (
                    node.func.attr not in levels
                    or not isinstance(node.func.value, ast.Name)
                    or node.func.value.id not in {"logger", "log", "logging"}
                ):
                    continue
                if not node.args:
                    raise DesignError(f"ログ本文がありません: {path}:{node.lineno}")
                event = node.args[0]
                rows.append(
                    [
                        node.func.attr.upper(),
                        event.value if isinstance(event, ast.Constant) else ast.unparse(event),
                        "; ".join(f"{kw.arg}={ast.unparse(kw.value)}" for kw in node.keywords),
                        name,
                        f"{path.relative_to(root)}:{node.lineno}",
                    ]
                )
    return document(
        f"ログメッセージ: {op.id}",
        [
            "実logger呼出を抽出する。HTTPのエラー本文や架空のログを、実装ログとして数えない。共有サービスのログはその経路を通る操作へ帰属させる。",
            table(["レベル", "メッセージ・イベント", "構造化項目", "発生関数", "実装位置"], rows)
            if rows
            else "対象のrouter・functions・共有操作サービスには、実装されたログ出力がない。",
            "[詳細設計](detail.md) / [エラー応答](interface.md)",
        ],
    )
