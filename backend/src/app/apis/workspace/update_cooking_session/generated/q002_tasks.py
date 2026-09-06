# app-docs による自動生成。直接編集しない。
# SQLのSHA256: b8e78720fbc3c5efaa7505e50ab304aeb6e9e03e07d5b59794570dd57c572052
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 進捗更新の対象は本人のセッションに属する既存工程だけにする。
SELECT
    t.id,
    t.menu_item_id,
    t.step_id,
    t.status,
    t.timer_started_at,
    t.timer_duration_s,
    t.planned_start_s,
    t.planned_end_s
FROM recipeweave.session_task AS t
INNER JOIN recipeweave.cooking_session AS s ON t.session_id = s.id
INNER JOIN recipeweave.menu AS m ON s.menu_id = m.id
WHERE t.session_id = %(session_id)s AND m.user_id = %(user_id)s
ORDER BY t.planned_start_s, t.id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("session_id", "user_id")}


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
