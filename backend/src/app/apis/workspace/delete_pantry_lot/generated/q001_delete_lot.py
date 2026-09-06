# app-docs による自動生成。直接編集しない。
# SQLのSHA256: c5cc28cf22b888ffe31265ff45e7e3cc9496366601afeb3e1061d500ab50d0e6
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 履歴と消費台帳の参照を保ったまま本人の在庫を無効化する。
UPDATE recipeweave.pantry_lot SET status = 'deleted', updated_at = CURRENT_TIMESTAMP
WHERE id = %(row_id)s AND user_id = %(user_id)s AND status = 'active' RETURNING id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("row_id", "user_id")}


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
