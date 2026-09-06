"""SQLGlotのDDL/DML構文木から物理テーブルとCRUDを抽出する。"""

import ast
import json
from dataclasses import dataclass, field
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


@dataclass
class Query:
    source: str
    operation: str
    sql: str
    actions: dict[str, set[str]]
    parameters: list[str]
    columns: dict[str, list[str]] = field(default_factory=dict)


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


def load_tables(root: Path) -> dict[str, Table]:
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


def query_projection(text: str, source: str, operation: str, tables: dict[str, Table]) -> Query:
    stmt = parse_one(text, source)
    kinds = {exp.Select: "R", exp.Insert: "C", exp.Update: "U", exp.Delete: "D"}
    action = next((value for kind, value in kinds.items() if isinstance(stmt, kind)), None)
    if action is None or stmt.find(exp.Star):
        raise DesignError(f"対応する明示列のCRUD文が必要です: {source}")
    references = list(stmt.find_all(exp.Table))
    aliases = {ref.alias_or_name: sql_name(ref) for ref in references}
    actions: dict[str, set[str]] = {}
    for ref in references:
        name = sql_name(ref)
        if name not in tables:
            raise DesignError(f"未定義テーブルです: {source}: {name}")
        actions.setdefault(name, set()).add("R")
    target = stmt.this.this if isinstance(stmt.this, exp.Schema) else stmt.this
    target_name = sql_name(target) if isinstance(target, exp.Table) else None
    if action != "R" and target_name:
        actions[target_name] = {action}
        if any(
            sql_name(ref) == target_name
            for select in stmt.find_all(exp.Select)
            for ref in select.find_all(exp.Table)
        ):
            actions[target_name].add("R")
    columns: dict[str, list[str]] = {}
    for column in stmt.find_all(exp.Column):
        candidates = [aliases.get(column.table, column.table)] if column.table else list(actions)
        matches = [
            name
            for name in candidates
            if name in tables and column.name in {c.name for c in tables[name].columns}
        ]
        if len(matches) != 1:
            raise DesignError(f"未定義または曖昧な列です: {source}: {column.sql()}")
        columns.setdefault(matches[0], []).append(column.name)
    if isinstance(stmt, exp.Insert) and isinstance(stmt.this, exp.Schema) and target_name:
        for col in stmt.this.expressions:
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
            "実DDLで作られる表だけを掲載する。JSON状態内の配列や将来の正規化テーブルは物理表として数えない。",
            table(["テーブル", "意味", "列数", "定義元"], rows),
            "[ER図](ER.md) / [APIとのCRUD](../api/CRUD.md)",
        ],
    )
    er = ["```mermaid", "erDiagram"]
    for name, item in sorted(tables.items()):
        alias = name.replace(".", "_")
        er.append(f"    {alias} {{")
        for col in item.columns:
            data_type = col.data_type.replace(" ", "_").replace("(", "_").replace(")", "")
            key = " PK" if any("PRIMARY KEY" in c for c in col.constraints) else ""
            er.append(f"        {data_type} {col.name}{key}")
        er.append("    }")
        for local, target, _ in item.foreign_keys:
            # この記号は外部キーの存在を示し、実データ件数を推定しない。
            er.append(f'    {target.replace(".", "_")} ||--o{{ {alias} : "{",".join(local)}"')
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
                "## 利用API\n\n"
                + (
                    table(["operationId", "CRUD", "SQL"], access)
                    if access
                    else "APIからのアクセスなし。マイグレーション実行時のみ利用する。"
                ),
            ],
        )
    return outputs
