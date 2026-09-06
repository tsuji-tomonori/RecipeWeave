# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 40c08978127d8527381e87538932ff53e13158dc8a2cd06104aee8d94ce67e20
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 消費・編集済み在庫を巻き戻さず、未使用の登録分だけを取り消す。
UPDATE recipeweave.pantry_lot AS p SET status = 'undone', updated_at = CURRENT_TIMESTAMP
WHERE
    p.source_import_id = %(row_id)s AND p.user_id = %(user_id)s AND NOT p.edited
    AND NOT EXISTS (
        SELECT 1 FROM recipeweave.pantry_consumption AS c
        WHERE c.lot_id = p.id
    )
RETURNING p.id;
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
