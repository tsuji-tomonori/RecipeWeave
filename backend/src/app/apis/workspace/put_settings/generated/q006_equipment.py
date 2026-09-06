# app-docs による自動生成。直接編集しない。
# SQLのSHA256: ed46cdb08d3473d847048df16b0e699f8169501398d263c9712e1cbc5888c96a
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 既存器具のID・容量・予約を保持して再有効化する。
UPDATE recipeweave.kitchen_resource AS kitchen
SET active = TRUE
FROM recipeweave.resource_type AS resource_kind
WHERE
    kitchen.user_id = %(user_id)s
    AND kitchen.resource_type_id = resource_kind.id
    AND resource_kind.name = %(name)s AND resource_kind.status = 'active'
RETURNING kitchen.id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("name", "user_id")}


def _execute(
    connection: Connection[dict[str, Any]], name: str, params: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """許可された固定SQLだけに、宣言と一致する束縛値を別渡しする。"""
    if name not in QUERIES or set(params) != set(PARAMETERS[name]):
        raise ValueError("SQL名または束縛パラメータが操作契約にありません")
    cursor = connection.execute(QUERIES[name], dict(params))
    return list(cursor.fetchall()) if cursor.description is not None else []


SQL = QUERIES["query"]


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """固定した単文SQLを実行する。"""
    return _execute(connection, "query", values)
