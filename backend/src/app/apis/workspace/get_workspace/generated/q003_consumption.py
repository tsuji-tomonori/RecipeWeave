# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 62abd118bc364c94d0e8a913bf32e9e90eee4f3b630b1f92bf8c0b1f0c33af7c
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 二重消費を防ぐ台帳からロットごとの使用履歴を読む。
SELECT
    c.lot_id,
    c.amount,
    u.code AS unit,
    c.session_id
FROM recipeweave.pantry_consumption AS c INNER JOIN recipeweave.unit AS u ON c.unit_id = u.id
WHERE c.user_id = %(user_id)s
ORDER BY c.created_at, c.id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("user_id",)}


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
