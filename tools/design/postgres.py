"""PostgreSQL文法で全移行を解析し、補助カタログの対象漏れを検出する。"""

import json
from pathlib import Path
from typing import Any

from pglast import parser

from .common import DesignError, read_source

SUPPORTED = {
    "CreateStmt",
    "CreateExtensionStmt",
    "CommentStmt",
    "AlterTableStmt",
    "IndexStmt",
    "CreateFunctionStmt",
    "CreateTrigStmt",
    "CreatePolicyStmt",
    "GrantStmt",
    "GrantRoleStmt",
    "CreateSchemaStmt",
    "VariableSetStmt",
    "DoStmt",
    "AlterDefaultPrivilegesStmt",
    "CreateRoleStmt",
}


def inspect_postgres(root: Path, catalog: dict[str, Any]) -> dict[str, Any]:
    """正規表現で拾った件数だけを信用せず、SQL文法木の実体と照合する。"""
    tables: dict[str, dict[str, Any]] = {}
    indexes: dict[str, set[str]] = {}
    foreign_keys: dict[str, set[str]] = {}
    contracts = []
    for path in sorted((root / "database/migrations").glob("*.sql")):
        source = read_source(path, root)
        try:
            statements = json.loads(parser.parse_sql_json(source))["stmts"]
        except Exception as exc:
            raise DesignError(f"PostgreSQLの移行構文を解析できません: {path}: {exc}") from exc
        for numbered, raw in enumerate(statements, 1):
            wrapper = raw["stmt"]
            kind = next(iter(wrapper))
            item = wrapper[kind]
            if kind not in SUPPORTED:
                raise DesignError(f"移行DDLの未対応構文: {path}:{numbered}: {kind}")
            source_name = f"{path.relative_to(root)}:statement-{numbered}"
            if kind == "CreateStmt":
                relation = item["relation"]
                if relation.get("schemaname") != "recipeweave":
                    raise DesignError(f"想定外スキーマの表です: {source_name}")
                name = relation["relname"]
                if name in tables:
                    raise DesignError(f"DDLの表が重複しています: {name}")
                columns = {
                    element["ColumnDef"]["colname"]
                    for element in item.get("tableElts", [])
                    if "ColumnDef" in element
                }
                tables[name] = {"source": source_name, "columns": columns, "ast": item}
            elif kind == "IndexStmt":
                indexes.setdefault(item["relation"]["relname"], set()).add(item["idxname"])
            elif kind == "AlterTableStmt":
                name = item["relation"]["relname"]
                for action in item.get("cmds", []):
                    command = action["AlterTableCmd"]
                    subtype = command.get("subtype")
                    if subtype == "AT_AddColumn":
                        tables[name]["columns"].add(command["def"]["ColumnDef"]["colname"])
                    elif subtype == "AT_DropColumn":
                        tables[name]["columns"].remove(command["name"])
                    if subtype == "AT_AddConstraint":
                        constraint = command["def"].get("Constraint", {})
                        if constraint.get("contype") == "CONSTR_FOREIGN":
                            foreign_keys.setdefault(name, set()).add(constraint["conname"])
            if kind != "CommentStmt":
                location = raw.get("stmt_location", 0)
                length = raw.get("stmt_len", 0)
                data = source.encode("utf-8")
                sql = data[location : location + length if length else None].decode("utf-8").strip()
                contracts.append({"source": source_name, "kind": kind, "ast": item, "sql": sql})
    projected = {table["name"]: table for table in catalog["tables"]}
    if set(tables) != set(projected):
        raise DesignError(f"DDL文法木とカタログの表集合が不一致: {set(tables) ^ set(projected)}")
    for name, item in tables.items():
        if item["columns"] != {column["name"] for column in projected[name]["columns"]}:
            raise DesignError(f"DDL文法木とカタログの列集合が不一致: {name}")
        if indexes.get(name, set()) != {index["name"] for index in projected[name]["indexes"]}:
            raise DesignError(f"DDL文法木とカタログの索引集合が不一致: {name}")
        if foreign_keys.get(name, set()) != {fk["name"] for fk in projected[name]["foreign_keys"]}:
            raise DesignError(f"DDL文法木とカタログの外部キー集合が不一致: {name}")
    return {"tables": tables, "statements": contracts}
