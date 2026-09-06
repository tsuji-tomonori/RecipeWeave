# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 6f359f4307d38f98cf56a1770221e375a261097164e763bd8194b82261ff360c
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 開始済みタイマーを再送でリセットしない。
UPDATE recipeweave.session_task SET
    timer_started_at = CURRENT_TIMESTAMP,
    timer_duration_s = planned_end_s - planned_start_s
WHERE id = %(row_id)s AND session_id = %(session_id)s AND timer_started_at IS NULL;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("row_id", "session_id")}


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
