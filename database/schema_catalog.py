"""適用対象DDLからテーブル・列・制約を抽出し、原設計との対応を検査する。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def split_sql(value: str, delimiter: str = ";") -> list[str]:
    """引用符、ドル引用と括弧内を保持してSQLを分割する。"""
    result: list[str] = []
    start = 0
    index = 0
    depth = 0
    quote: str | None = None
    while index < len(value):
        if quote:
            if value.startswith(quote, index):
                if quote == "'" and value.startswith("''", index):
                    index += 2
                    continue
                index += len(quote)
                quote = None
                continue
        elif value.startswith("--", index):
            newline = value.find("\n", index)
            index = len(value) if newline < 0 else newline
            continue
        elif value[index] == "'":
            quote = "'"
        elif value[index] == "$":
            match = re.match(r"\$[A-Za-z_0-9]*\$", value[index:])
            if match:
                quote = match.group()
                index += len(quote)
                continue
        elif value[index] == "(":
            depth += 1
        elif value[index] == ")":
            depth -= 1
        elif value[index] == delimiter and depth == 0:
            item = value[start:index].strip()
            if item:
                result.append(item)
            start = index + 1
        index += 1
    if quote or depth:
        raise ValueError("SQLの引用または括弧が閉じていません")
    if value[start:].strip():
        result.append(value[start:].strip())
    return result


def squash_sql(value: str) -> str:
    """引用された値を保持して、構造の空白だけを正規化する。"""
    tokens = re.findall(r"'(?:[^']|'')*'|\"(?:[^\"]|\"\")*\"|\s+|[^'\"\s]+", value)
    return "".join(" " if token.isspace() else token for token in tokens).strip()


def unquote(value: str) -> str:
    return value[1:-1].replace("''", "'")


def extract(root: Path = ROOT) -> dict[str, Any]:
    """構造はDDL、説明はCOMMENT、所有・保持区分は明示方針から導出する。"""
    policy_document = json.loads((root / "database/schema-policy.json").read_text())
    policy = policy_document["tables"]
    sources = sorted((root / "database/migrations").glob("*.sql"))
    tables: dict[str, dict[str, Any]] = {}
    statements: list[str] = []
    statement_sources: list[dict[str, Any]] = []
    for path in sources:
        content = re.sub(r"^\s*--[^\n]*", "", path.read_text(), flags=re.MULTILINE)
        for number, statement in enumerate(split_sql(content), 1):
            statements.append(statement)
            statement_sources.append(
                {
                    "file": str(path.relative_to(root)),
                    "number": number,
                    "sha256": hashlib.sha256(statement.encode()).hexdigest(),
                    "sql": statement,
                }
            )
            statement = squash_sql(statement)
            match = re.fullmatch(
                r"CREATE TABLE recipeweave\.([a-z_][a-z_0-9]*)\s*\((.*)\)", statement, re.DOTALL
            )
            if not match:
                continue
            name, body = match.groups()
            if name in tables:
                raise ValueError(f"重複テーブル: {name}")
            info: dict[str, Any] = {
                "name": name,
                "description": "",
                "source": dict(statement_sources[-1]),
                "columns": [],
                "primary_key": [],
                "unique_constraints": [],
                "foreign_keys": [],
                "checks": [],
                "indexes": [],
                **policy.get(
                    name, {"retention": "legacy", "domain": "移行互換", "owner_path": None}
                ),
            }
            for clause in split_sql(body, ","):
                if clause.startswith("CHECK ("):
                    info["checks"].append(squash_sql(clause[7:-1]))
                    continue
                if clause.startswith("UNIQUE"):
                    info["unique_constraints"].append(
                        {
                            "columns": [
                                x.strip().strip(chr(34))
                                for x in clause[clause.index("(") + 1 : -1].split(",")
                            ],
                            "nulls_not_distinct": "NULLS NOT DISTINCT" in clause,
                            "definition": clause,
                        }
                    )
                    continue
                column_match = re.fullmatch(
                    r'("?[a-z_][a-z_0-9]*"?)\s+([A-Z]+(?:\([0-9, ]+\))?(?:\[\])?)(.*)',
                    clause,
                    re.DOTALL,
                )
                if not column_match:
                    raise ValueError(f"未対応の列宣言: {name}: {clause}")
                column, datatype, suffix = column_match.groups()
                column = column.strip(chr(34))
                primary = "PRIMARY KEY" in suffix
                default = re.search(r"DEFAULT\s+(.+)", suffix)
                info["columns"].append(
                    {
                        "name": column,
                        "type": datatype.lower().replace(" ", ""),
                        "nullable": "NOT NULL" not in suffix and not primary,
                        "default": default.group(1).strip() if default else None,
                        "primary_key": primary,
                        "description": "",
                        "enum": [],
                        "checks": [],
                    }
                )
                if primary:
                    info["primary_key"].append(column)
            tables[name] = info
    for statement in statements:
        statement = squash_sql(statement)
        addition = re.fullmatch(
            r"ALTER TABLE recipeweave\.([a-z_][a-z_0-9]*) "
            r"ADD COLUMN ([a-z_][a-z_0-9]*) ([A-Z]+(?:\([0-9, ]+\))?)(.*)",
            statement,
            re.DOTALL,
        )
        if addition:
            table, name, datatype, suffix = addition.groups()
            default = re.search(r"DEFAULT\s+(.+)", suffix)
            tables[table]["columns"].append(
                {
                    "name": name,
                    "type": datatype.lower().replace(" ", ""),
                    "nullable": "NOT NULL" not in suffix,
                    "default": default.group(1).strip() if default else None,
                    "primary_key": False,
                    "description": "",
                    "enum": [],
                    "checks": [],
                    "source_origin": "service-extension",
                }
            )
            continue
        nullable = re.fullmatch(
            r"ALTER TABLE recipeweave\.([a-z_][a-z_0-9]*) "
            r"ALTER COLUMN ([a-z_][a-z_0-9]*) DROP NOT NULL",
            statement,
        )
        if nullable:
            table, name = nullable.groups()
            next(c for c in tables[table]["columns"] if c["name"] == name)["nullable"] = True
            continue
        extra_check = re.fullmatch(
            r"ALTER TABLE recipeweave\.([a-z_][a-z_0-9]*) ADD CONSTRAINT [a-z_0-9]+ CHECK \((.*)\)",
            statement,
            re.DOTALL,
        )
        if extra_check:
            table, expression = extra_check.groups()
            if table == "cooking_session" and expression.startswith("status IN"):
                tables[table]["checks"] = [
                    c for c in tables[table]["checks"] if not c.startswith("status IN")
                ]
            tables[table]["checks"].append(expression)
            continue
        comment = re.fullmatch(
            r"COMMENT ON (TABLE|COLUMN) recipeweave\.([a-z_][a-z_0-9]*)"
            r"(?:\.(\"?[a-z_][a-z_0-9]*\"?))? IS ('(?:[^']|'')*')",
            statement,
            re.DOTALL,
        )
        if comment:
            kind, name, column, description = comment.groups()
            column = column.strip(chr(34)) if column else None
            item = tables[name]
            if kind == "TABLE":
                item["description"] = unquote(description)
            else:
                next(c for c in item["columns"] if c["name"] == column)["description"] = unquote(
                    description
                )
            continue
        foreign = re.fullmatch(
            r"ALTER TABLE recipeweave\.([a-z_][a-z_0-9]*) "
            r"ADD CONSTRAINT ([a-z_][a-z_0-9]*)\s+FOREIGN KEY \(([^)]+)\) "
            r"REFERENCES recipeweave\.([a-z_][a-z_0-9]*) \(([^)]+)\)\s+"
            r"ON DELETE (RESTRICT|CASCADE|SET NULL) "
            r"ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED",
            statement,
            re.DOTALL,
        )
        if foreign:
            name, constraint, columns, parent, target, action = foreign.groups()
            tables[name]["foreign_keys"].append(
                {
                    "name": constraint,
                    "columns": [x.strip() for x in columns.split(",")],
                    "referenced_table": parent,
                    "referenced_columns": [x.strip() for x in target.split(",")],
                    "on_delete": action,
                    "on_update": "RESTRICT",
                    "deferrable": True,
                    "initially_deferred": True,
                    "definition": statement,
                }
            )
            continue
        index = re.fullmatch(
            r"CREATE (UNIQUE )?INDEX ([a-z_0-9]+) ON recipeweave\.([a-z_][a-z_0-9]*) (.*)",
            statement,
            re.DOTALL,
        )
        if index:
            unique, name, table, expression = index.groups()
            tables[table]["indexes"].append(
                {"name": name, "unique": bool(unique), "definition": expression, "sql": statement}
            )
    for item in tables.values():
        table_checks: list[str] = item["checks"]
        for column in item["columns"]:
            column_name: str = column["name"]
            column_checks: list[str] = [
                check
                for check in table_checks
                if re.search(r"\b" + re.escape(column_name) + r"\b", check)
            ]
            column["checks"] = column_checks
            for check in column_checks:
                length_limit = re.fullmatch(
                    r"CHAR_LENGTH\(" + re.escape(column_name) + r"\) <= ([0-9]+)",
                    check,
                    re.IGNORECASE,
                )
                if length_limit:
                    column["max_length"] = min(
                        column.get("max_length", int(length_limit[1])), int(length_limit[1])
                    )
                enum = re.fullmatch(re.escape(column_name) + r" IN \((.*)\)", check)
                if enum:
                    column["enum"] = [unquote(x.strip()) for x in split_sql(enum.group(1), ",")]
        for foreign in item["foreign_keys"]:
            if foreign["referenced_table"] not in tables:
                raise ValueError(f"未定義のFK参照先: {foreign}")
    source = json.loads((root / "spec/database/source-sheet.json").read_text())
    expected = source["tabs"]["02_カラム辞書"][1:]
    for table, _, column, kind, null, *_ in expected:
        actual = next((c for c in tables[table]["columns"] if c["name"] == column), None)
        if (
            actual is None
            or actual["type"] != kind
            or actual["nullable"]
            != policy_document.get("column_evolutions", {})
            .get(f"{table}.{column}", {})
            .get("nullable", null == "可")
        ):
            raise ValueError(f"原設計との差異: {table}.{column}")
    return {
        "schemaVersion": 1,
        "schema": "recipeweave",
        "source_table_count": source["tableCount"],
        "source_column_count": source["columnCount"],
        "column_evolutions": policy_document.get("column_evolutions", {}),
        "sources": [
            {
                "path": str(path.relative_to(root)),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
            for path in sources
        ],
        "tables": list(tables.values()),
        "statements": statement_sources,
        "database_contracts": [
            s
            for s in statements
            if s.startswith(
                (
                    "CREATE FUNCTION",
                    "CREATE CONSTRAINT TRIGGER",
                    "CREATE TRIGGER",
                    "CREATE POLICY",
                    "ALTER TABLE",
                )
            )
            and "FOREIGN KEY" not in s
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    output = ROOT / "database/schema_catalog.json"
    text = json.dumps(extract(), ensure_ascii=False, indent=2) + "\n"
    if arguments.check:
        if not output.exists() or output.read_text() != text:
            raise SystemExit("DBスキーマカタログに生成差分があります")
    else:
        output.write_text(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
