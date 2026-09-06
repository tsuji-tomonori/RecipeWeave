"""pglastのDDLとSQLGlotのDML構文木から物理テーブルとCRUDを抽出する。"""

import ast
import json
import re
from dataclasses import dataclass, field, replace
from pathlib import Path

import sqlglot
from sqlglot import exp

from .common import DesignError, document, read_source, table


@dataclass
class Column:
    name: str
    data_type: str
    nullable: bool
    constraints: list[str]
    default: str
    description: str = ""


@dataclass
class Table:
    name: str
    source: str
    columns: list[Column]
    constraints: list[str]
    foreign_keys: list[tuple[list[str], str, list[str]]]
    description: str = ""
    indexes: list[dict] = field(default_factory=list)
    foreign_key_specs: list[dict] = field(default_factory=list)
    domain: str = "共通"
    retention: str = "未指定"


@dataclass
class Query:
    source: str
    operation: str
    sql: str
    actions: dict[str, set[str]]
    parameters: list[str]
    columns: dict[str, list[str]] = field(default_factory=dict)
    condition: str = "このSQLの呼出し経路で実行"
    transaction_effect: str | None = None


def sql_name(node: exp.Table) -> str:
    return ".".join(part for part in (node.catalog, node.db, node.name) if part)


def parse_one(text: str, source: str) -> exp.Expression:
    try:
        statements = [item for item in sqlglot.parse(text, read="postgres") if item is not None]
    except sqlglot.errors.ParseError as exc:
        raise DesignError(f"SQLを解析できません: {source}: {exc}") from exc
    if len(statements) != 1 or isinstance(statements[0], exp.Command):
        raise DesignError(f"単一の対応SQL文が必要です: {source}")
    return statements[0]


def ddl_sources(root: Path) -> list[tuple[str, str]]:
    sources = [
        (str(p.relative_to(root)), read_source(p, root))
        for p in sorted((root / "database/migrations").glob("*.sql"))
    ]
    migration = root / "database/migrate.py"
    tree = ast.parse(read_source(migration, root))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr != "execute" or not node.args:
            continue
        value = node.args[0]
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            # 文の種類は字句で絞り、構造の解釈は下流のSQL ASTに限定する。
            tokens = sqlglot.tokenize(value.value, read="postgres")
            if len(tokens) >= 2 and [t.text.upper() for t in tokens[:2]] == ["CREATE", "TABLE"]:
                sources.append((f"database/migrate.py:{node.lineno}", value.value))
    return sources


def project_table(statement: exp.Expression, source: str) -> Table | None:
    if not isinstance(statement, exp.Create):
        raise DesignError(f"DDL投影が未対応の文です: {source}: {type(statement).__name__}")
    if statement.args.get("kind") != "TABLE":
        raise DesignError(f"テーブル以外の移行DDLは個別対応が必要です: {source}")
    schema = statement.this
    if not isinstance(schema, exp.Schema) or not isinstance(schema.this, exp.Table):
        raise DesignError(f"静的な列定義を持つCREATE TABLEが必要です: {source}")
    columns = []
    constraints = []
    foreign_keys = []
    for item in schema.expressions:
        if isinstance(item, exp.ColumnDef):
            rules = list(item.args.get("constraints", []))
            if any(rule.find(exp.Reference) for rule in rules):
                raise DesignError(
                    f"列内REFERENCESは未対応です。表制約として記述してください: {source}"
                )
            default = next(
                (
                    r.args["kind"].this.sql(dialect="postgres")
                    for r in rules
                    if isinstance(r.args["kind"], exp.DefaultColumnConstraint)
                ),
                "なし",
            )
            nullable = not any(
                isinstance(
                    r.args["kind"], exp.NotNullColumnConstraint | exp.PrimaryKeyColumnConstraint
                )
                for r in rules
            )
            columns.append(
                Column(
                    item.name,
                    item.args["kind"].sql(dialect="postgres"),
                    nullable,
                    [r.sql(dialect="postgres") for r in rules],
                    default,
                )
            )
        else:
            constraints.append(item.sql(dialect="postgres"))
        for fk in item.find_all(exp.ForeignKey):
            reference = fk.args.get("reference")
            if reference is None or not isinstance(reference.this, exp.Schema):
                raise DesignError(f"参照先の列を持たない外部キーは未対応です: {source}")
            target = reference.this
            if not isinstance(target.this, exp.Table):
                raise DesignError(f"外部キーの参照先が不正です: {source}")
            foreign_keys.append(
                (
                    [c.name for c in fk.expressions],
                    sql_name(target.this),
                    [c.name for c in target.expressions],
                )
            )
    # テーブルレベルの主キーもnullableへ反映する。
    primary = {
        c.name
        for item in schema.expressions
        if not isinstance(item, exp.ColumnDef)
        for pk in item.find_all(exp.PrimaryKey)
        for c in pk.expressions
    }
    for col in columns:
        if col.name in primary:
            col.nullable = False
            col.constraints.append("PRIMARY KEY（表制約）")
    if len({c.name for c in columns}) != len(columns):
        raise DesignError(f"列名が重複しています: {source}")
    return Table(sql_name(schema.this), source, columns, constraints, foreign_keys)


def load_legacy_tables(root: Path) -> dict[str, Table]:
    tables: dict[str, Table] = {}
    for source, text in ddl_sources(root):
        item = project_table(parse_one(text, source), source)
        if item is None:
            continue
        if item.name in tables:
            raise DesignError(f"テーブルの定義が重複しています: {item.name}")
        tables[item.name] = item
    metadata = json.loads(read_source(root / "database/design.manual.json", root))
    if metadata.get("schemaVersion") != 1 or set(metadata["tables"]) != set(tables):
        raise DesignError("DDLと説明メタデータのテーブル集合が一致しません")
    for name, item in tables.items():
        description = metadata["tables"][name]
        if set(description["columns"]) != {c.name for c in item.columns}:
            raise DesignError(f"DDLと説明メタデータの列集合が一致しません: {name}")
        item.description = description["description"]
        for col in item.columns:
            col.description = description["columns"][col.name]
            if not col.description.strip():
                raise DesignError(f"列の説明が空です: {name}.{col.name}")
        for local, target, remote in item.foreign_keys:
            if target not in tables or len(local) != len(remote):
                raise DesignError(f"外部キー参照が不正です: {name} -> {target}")
            if not set(local) <= {c.name for c in item.columns} or not set(remote) <= {
                c.name for c in tables[target].columns
            }:
                raise DesignError(f"外部キーの列が存在しません: {name} -> {target}")
    return tables


def load_tables(root: Path) -> dict[str, Table]:
    if not (root / "database/schema-policy.json").exists():
        return load_legacy_tables(root)
    from database.schema_catalog import extract

    from .postgres import inspect_postgres

    catalog = extract(root)
    projection = inspect_postgres(root, catalog)
    tables = {}
    for item in catalog["tables"]:
        name = "recipeweave." + item["name"]
        columns = [
            Column(
                col["name"],
                col["type"],
                col["nullable"],
                (["PRIMARY KEY"] if col["primary_key"] else []) + col["checks"],
                str(col["default"]) if col["default"] is not None else "なし",
                col["description"],
            )
            for col in item["columns"]
        ]
        constraints = ["CHECK (" + text + ")" for text in item["checks"]]
        constraints += [
            "UNIQUE "
            + ("NULLS NOT DISTINCT " if value.get("nulls_not_distinct") else "")
            + "("
            + ", ".join(value["columns"])
            + ")"
            for value in item["unique_constraints"]
        ]
        constraints += ["PRIMARY KEY (" + ", ".join(item["primary_key"]) + ")"]
        tables[name] = Table(
            name,
            projection["tables"][item["name"]]["source"],
            columns,
            constraints,
            [
                (fk["columns"], "recipeweave." + fk["referenced_table"], fk["referenced_columns"])
                for fk in item["foreign_keys"]
            ],
            item["description"],
            item["indexes"],
            item["foreign_keys"],
            item.get("domain", "共通"),
            item.get("retention", "未指定"),
        )
    # 移行台帳はPython内の実CREATE文から従来同様に取り込む。
    for source, text in ddl_sources(root):
        if source.startswith("database/migrate.py:"):
            item = project_table(parse_one(text, source), source)
            if item is not None:
                metadata = json.loads(read_source(root / "database/design.manual.json", root))[
                    "tables"
                ][item.name]
                item.description = metadata["description"]
                for column in item.columns:
                    column.description = metadata["columns"][column.name]
                tables[item.name] = item
    return tables


def constraint_mode(text: str, source: str) -> bool | None:
    """制約検証モードの固定2文だけをPostgreSQLの実構文で判定する。"""
    tokens = sqlglot.tokenize(text, read="postgres")
    if [token.text.upper() for token in tokens[:2]] != ["SET", "CONSTRAINTS"]:
        return None
    from pglast import ast as postgres_ast
    from pglast import parse_sql
    from pglast.parser import ParseError

    try:
        statements = parse_sql(text)
    except ParseError as exc:
        raise DesignError(f"制約検証モードのSQLが不正です: {source}: {exc}") from exc
    if (
        len(statements) != 1
        or not isinstance(statements[0].stmt, postgres_ast.ConstraintsSetStmt)
        or statements[0].stmt.constraints is not None
    ):
        raise DesignError(f"制約検証モードはSET CONSTRAINTS ALLの単文だけを扱います: {source}")
    return bool(statements[0].stmt.deferred)


def query_projection(text: str, source: str, operation: str, tables: dict[str, Table]) -> Query:
    deferred = constraint_mode(text, source)
    if deferred is not None:
        return Query(
            source,
            operation,
            text,
            {},
            [],
            transaction_effect=(
                "遅延可能な制約の検査をトランザクション終了まで遅延する。"
                if deferred
                else "保留していた遅延可能な制約を直ちに検査し、以後も即時検査する。"
            ),
        )
    stmt = parse_one(text, source)
    kinds = {
        exp.Select: "R",
        exp.SetOperation: "R",
        exp.Insert: "C",
        exp.Update: "U",
        exp.Delete: "D",
    }
    action = next((value for kind, value in kinds.items() if isinstance(stmt, kind)), None)
    if action is None or stmt.find(exp.Star):
        raise DesignError(f"対応する明示列のCRUD文が必要です: {source}")
    conflict = stmt.args.get("conflict")
    if conflict is not None and str(conflict.args.get("action")) not in {"DO NOTHING", "DO UPDATE"}:
        raise DesignError(f"対応しない競合時処理です: {source}")
    if any(
        isinstance(node, exp.Insert | exp.Update | exp.Delete) and node is not stmt
        for node in stmt.walk()
    ):
        raise DesignError(f"入れ子のDML投影は未対応です: {source}")
    from sqlglot.optimizer.qualify import qualify
    from sqlglot.optimizer.scope import Scope, traverse_scope

    projection_input = stmt.copy()
    for lock in list(projection_input.find_all(exp.Lock)):
        owner = lock.find_ancestor(exp.Select)
        names = (
            {
                ref.alias_or_name
                for ref in owner.find_all(exp.Table)
                if ref.find_ancestor(exp.Select) is owner and not isinstance(ref.parent, exp.Lock)
            }
            if owner is not None
            else set()
        )
        for ref in lock.expressions:
            if not isinstance(ref, exp.Table) or ref.name not in names:
                raise DesignError(f"行ロック対象の別名が存在しません: {source}: {ref.sql()}")
        # SQLGlotがFOR SHARE OFの別名をFROMの重複表と数えるため、
        # 実在確認後の列投影では除く。SQL仕様と詳細設計には元のロック句を保持する。
        lock.pop()
    schema = {}
    for name, item in tables.items():
        namespace, short = name.rsplit(".", 1)
        schema.setdefault(namespace, {})[short] = {c.name: c.data_type for c in item.columns} | {
            "xmin": "xid"
        }
    try:
        resolved = qualify(
            projection_input,
            dialect="postgres",
            schema=schema,
            infer_schema=False,
            validate_qualify_columns=True,
        )
    except sqlglot.errors.SqlglotError as exc:
        raise DesignError(f"SQL列の名前解決に失敗しました: {source}: {exc}") from exc
    cte_names = {cte.alias for cte in resolved.find_all(exp.CTE)}
    references = [
        ref for ref in resolved.find_all(exp.Table) if ref.db or ref.name not in cte_names
    ]
    aliases = {ref.alias_or_name: sql_name(ref) for ref in references}
    actions: dict[str, set[str]] = {}
    for ref in references:
        name = sql_name(ref)
        if name not in tables:
            raise DesignError(f"未定義テーブルです: {source}: {name}")
        actions.setdefault(name, set()).add("R")
    target = resolved.this.this if isinstance(resolved.this, exp.Schema) else resolved.this
    target_name = sql_name(target) if isinstance(target, exp.Table) else None
    if action != "R" and target_name:
        actions[target_name] = {action}
        if conflict is not None and conflict.args.get("expressions"):
            actions[target_name].add("U")
        if any(
            sql_name(ref) == target_name
            for select in resolved.find_all(exp.Select)
            for ref in select.find_all(exp.Table)
        ):
            actions[target_name].add("R")
    columns: dict[str, list[str]] = {}
    scopes = {id(scope.expression): scope for scope in traverse_scope(resolved)}
    output_aliases = {alias.alias for alias in resolved.find_all(exp.Alias)}
    for column in resolved.find_all(exp.Column):
        parent = column.find_ancestor(exp.Select)
        scope = scopes.get(id(parent)) if parent is not None else None
        selected = None
        current = scope
        while current is not None and selected is None:
            selected = current.sources.get(column.table)
            current = current.parent
        if isinstance(selected, Scope):
            # 派生表の列はqualifyが検査し、元表の列はそのscopeの実Columnから別途拾う。
            continue
        if isinstance(selected, exp.Table):
            candidates = [sql_name(selected)]
        elif column.table == "excluded" and conflict is not None and target_name:
            # EXCLUDEDは競合したINSERT候補行であり、独立した物理テーブルではない。
            candidates = [target_name]
        elif column.table:
            if column.table not in aliases:
                # UNNEST等の表関数の出力。qualifyで宣言名との一致を確認済み。
                continue
            candidates = [aliases[column.table]]
        elif target_name:
            candidates = [target_name]
        else:
            candidates = list(actions)
        matches = [
            name
            for name in candidates
            if name in tables and column.name in ({c.name for c in tables[name].columns} | {"xmin"})
        ]
        if (
            not column.table
            and column.name in output_aliases
            and isinstance(column.parent, exp.Ordered)
        ):
            continue
        if len(matches) != 1:
            raise DesignError(f"未定義または曖昧な列です: {source}: {column.sql()}")
        columns.setdefault(matches[0], []).append(column.name)
    if isinstance(resolved, exp.Insert) and isinstance(resolved.this, exp.Schema) and target_name:
        for col in resolved.this.expressions:
            if col.name not in {c.name for c in tables[target_name].columns}:
                raise DesignError(f"INSERT先の列が存在しません: {source}: {col.name}")
            columns.setdefault(target_name, []).append(col.name)
    parameters = sorted({str(p.this) for p in stmt.find_all(exp.Placeholder) if p.this})
    return Query(
        source,
        operation,
        text,
        actions,
        parameters,
        {name: sorted(set(cols)) for name, cols in columns.items()},
    )


def load_queries(root: Path, tables: dict[str, Table], slugs: dict[str, str]) -> list[Query]:
    result = []
    for path in sorted((root / "backend/src/app/apis").rglob("*.sql")):
        relative = path.relative_to(root / "backend/src/app/apis")
        if len(relative.parts) != 4 or relative.parts[2] != "sql":
            raise DesignError(f"SQLはAPI操作のsql/に配置してください: {relative}")
        slug = "/".join(relative.parts[:2])
        if slug not in slugs:
            raise DesignError(f"SQLの所有APIが存在しません: {relative}")
        result.append(
            query_projection(
                read_source(path, root), str(path.relative_to(root)), slugs[slug], tables
            )
        )
    inventory = root / "backend/src/app/entities/operation_inventory.json"
    if inventory.exists():
        data = json.loads(read_source(inventory, root))
        entries = data.get("operations", []) if isinstance(data, dict) else data
        for operation in entries:
            if operation["action"] not in {"create", "update", "delete"}:
                continue
            for filename in ("audit.sql", "outbox.sql", "workspace.sql"):
                if filename == "outbox.sql" and operation["owned"]:
                    continue
                if filename == "workspace.sql" and not operation["owned"]:
                    continue
                path = root / "backend/src/app/entities/sql" / filename
                result.append(
                    query_projection(
                        read_source(path, root),
                        str(path.relative_to(root)),
                        operation["operation_id"],
                        tables,
                    )
                )
    for slug, operation in sorted(slugs.items()):
        if slug.startswith("generation/"):
            for filename in ("audit.sql", "outbox.sql"):
                path = root / "backend/src/app/entities/sql" / filename
                result.append(
                    query_projection(
                        read_source(path, root), str(path.relative_to(root)), operation, tables
                    )
                )
    # 共通の応答集約やカタログ取得も、実装の呼出しを確認して元SQLへ対応づける。
    from types import SimpleNamespace

    from .details import operation_sources, selected_functions

    direct_queries = list(result)
    for slug, operation in sorted(slugs.items()):
        if not slug.startswith(("workspace/", "backup/")):
            continue
        op = SimpleNamespace(slug=slug, directory=root / "backend/src/app/apis" / slug)
        functions = [
            fn
            for path in operation_sources(root, op)
            for _, fn in selected_functions(root, op, path)
        ]
        shared = set()
        if slug != "workspace/get_workspace" and any(
            fn.name == "get_workspace" for fn in functions
        ):
            shared.add("get_workspace")
        if any(
            isinstance(call, ast.Call)
            and isinstance(call.func, ast.Attribute)
            and call.func.attr in {"finish", "get_workspace"}
            and ast.unparse(call.func.value) == "self.workspace"
            for fn in functions
            for call in ast.walk(fn)
        ):
            shared.add("get_workspace")
        for fn in functions:
            for call in ast.walk(fn):
                if not (
                    isinstance(call, ast.Call)
                    and isinstance(call.func, ast.Attribute)
                    and call.func.attr == "recipes"
                ):
                    continue
                argument = next((kw.value for kw in call.keywords if kw.arg == "operation"), None)
                if not isinstance(argument, ast.Constant) or not isinstance(argument.value, str):
                    raise DesignError(f"共有カタログの操作名が固定されていません: {slug}")
                shared.add(argument.value)
        for target in sorted(shared):
            matched = [query for query in direct_queries if query.operation == target]
            if not matched:
                raise DesignError(f"共有呼出しのSQLがありません: {slug}: {target}")
            result.extend(
                replace(
                    query,
                    operation=operation,
                    condition=f"共有処理 {target} を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。",
                )
                for query in matched
            )
    authentication = [query for query in result if "/auth/get_me/sql/" in query.source]
    for slug, operation in sorted(slugs.items()):
        if slug.startswith(("entities/", "workspace/", "generation/", "backup/")):
            result.extend(
                replace(
                    query,
                    operation=operation,
                    condition=(
                        "認証依存の初期化時。同一主体の初回INSERTのみ作成し、既存行はDO NOTHING。"
                    ),
                )
                for query in authentication
            )
        elif slug.startswith("recipes/"):
            result.extend(
                replace(
                    query,
                    operation=operation,
                    condition=(
                        "preview=true、または料理詳細でBearer認証を指定した場合。"
                        "認証なしの公開検索では実行しない。"
                        if slug == "recipes/get_recipe"
                        else "試用を許可した開発環境でpreview=trueとして認証する場合のみ。"
                        "通常の公開検索では実行しない。"
                    ),
                )
                for query in authentication
            )
    return result


def render_database(tables: dict[str, Table], queries: list[Query]) -> dict[str, str]:
    outputs = {}
    rows = [
        [f"[{name}](tables/{name}.md)", item.description, len(item.columns), item.source]
        for name, item in sorted(tables.items())
    ]
    outputs["database/README.md"] = document(
        "物理テーブル一覧",
        [
            "全マイグレーションの実DDLと移行台帳のCREATE文で作られる表を掲載する。"
            "原設計との対応は [原設計との対応](SOURCE-MAPPING.md)、"
            "トリガー・RLS等は [DB制約と手続き](CONTRACTS.md) から確認できる。",
            table(["テーブル", "意味", "列数", "定義元"], rows),
            "[ER図](ER.md) / [APIとのCRUD](../api/CRUD.md)",
        ],
    )
    er = ["```mermaid", "erDiagram"]
    for name, item in sorted(tables.items()):
        alias = name.replace(".", "_")
        er.append(f"    {alias} {{")
        for col in item.columns:
            data_type = re.sub(r"[^A-Za-z0-9_]", "_", col.data_type)
            key = " PK" if any("PRIMARY KEY" in c for c in col.constraints) else ""
            er.append(f"        {data_type} {col.name}{key}")
        er.append("    }")
        for local, target, _ in item.foreign_keys:
            required = all(not column.nullable for column in item.columns if column.name in local)
            parent_end = "||" if required else "|o"
            # 子側の最大件数はFK列全体の一意制約の有無から導く。
            primary = {
                column.name
                for column in item.columns
                if any("PRIMARY KEY" in rule for rule in column.constraints)
            }
            unique = set(local) == primary or any(
                rule.startswith("UNIQUE")
                and set(re.findall(r"[a-z_][a-z_0-9]*", rule.partition("(")[2])) == set(local)
                for rule in item.constraints
            )
            child_end = "o|" if unique else "o{"
            er.append(
                f"    {target.replace('.', '_')} {parent_end}--{child_end} {alias} : "
                f'"{",".join(local)}"'
            )
    er.append("```")
    outputs["database/ER.md"] = document(
        "物理ER図",
        [
            "\n".join(er),
            (
                "現在のDDLには外部キーがないため、表同士を結ぶ線はない。payloadの論理構造はAPIモデル仕様を参照する。"
                if not any(t.foreign_keys for t in tables.values())
                else "線はDDLの外部キー定義に基づく。"
                "実データの件数やアプリ上の関連を追加推測しない。"
            ),
        ],
    )
    for name, item in sorted(tables.items()):
        access = [
            [q.operation, ",".join(sorted(q.actions[name])), q.source]
            for q in queries
            if name in q.actions
        ]
        outputs[f"database/tables/{name}.md"] = document(
            f"テーブル仕様: {name}",
            [
                item.description,
                f"定義元: `{item.source}`",
                table(
                    ["列", "型", "NULL許可", "既定値", "制約", "意味"],
                    [
                        [
                            c.name,
                            c.data_type,
                            "可" if c.nullable else "不可",
                            c.default,
                            "; ".join(c.constraints) or "なし",
                            c.description,
                        ]
                        for c in item.columns
                    ],
                ),
                "## 表制約\n\n"
                + ("\n".join(f"- `{c}`" for c in item.constraints) or "列制約以外の追加制約なし。"),
                "## 索引\n\n"
                + (
                    table(
                        ["名称", "一意", "定義"],
                        [
                            [index["name"], index["unique"], index["definition"]]
                            for index in item.indexes
                        ],
                    )
                    if item.indexes
                    else "独立索引なし。主キー・一意制約の索引は表制約を参照。"
                ),
                "## 外部キー\n\n"
                + (
                    table(
                        ["名称", "列", "参照先", "削除", "更新", "遅延検査"],
                        [
                            [
                                fk["name"],
                                ", ".join(fk["columns"]),
                                fk["referenced_table"]
                                + "("
                                + ", ".join(fk["referenced_columns"])
                                + ")",
                                fk["on_delete"],
                                fk.get("on_update", "RESTRICT"),
                                fk.get("deferrable", False),
                            ]
                            for fk in item.foreign_key_specs
                        ],
                    )
                    if item.foreign_key_specs
                    else "外部キーなし。"
                ),
                "保持・所属領域: " + item.retention + " / " + item.domain,
                "## 利用API\n\n"
                + (
                    table(["operationId", "CRUD", "SQL"], access)
                    if access
                    else "APIからのアクセスなし。運用上の用途・旧表の保持は定義元を参照する。"
                ),
            ],
        )
    return outputs
