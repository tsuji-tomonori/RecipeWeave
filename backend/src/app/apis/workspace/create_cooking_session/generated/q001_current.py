# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 30ec6077ef4357122f120efc6402f2412080cf4349adf6c7668d161f9f4a0f8e
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 本人の進行中セッションを確認する。
SELECT
    s.id,
    s.menu_id,
    s.status,
    s.current_task_index
FROM recipeweave.cooking_session AS s
INNER JOIN
    recipeweave.menu AS m
    ON s.menu_id = m.id
WHERE
    m.user_id = %(user_id)s
    AND s.status IN ('planned', 'cooking', 'paused')
ORDER BY s.created_at DESC;
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
