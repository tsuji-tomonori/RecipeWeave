# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 2bb3bc45473bcde2d0919d5e9a8611096db7800ad3651ace1cc7448bd4b2bef6
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 在庫の減算と台帳の追記は同じ要求トランザクションで確定する。
UPDATE recipeweave.pantry_lot SET amount = amount - %(amount)s, updated_at = CURRENT_TIMESTAMP
WHERE id = %(lot_id)s AND user_id = %(user_id)s AND amount >= %(amount)s RETURNING id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("amount", "lot_id", "user_id")}


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
