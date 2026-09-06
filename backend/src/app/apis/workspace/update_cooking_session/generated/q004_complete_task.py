# app-docs による自動生成。直接編集しない。
# SQLのSHA256: a7d1bbda58224d93ce914c3afbff9eb2a1bf169ca5ae1ecd577642d3c5fe1f81
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 確認した工程を完了にし、最初の開始・完了時刻を保持する。
UPDATE recipeweave.session_task SET
    status = 'completed',
    actual_start_at = COALESCE(actual_start_at, CURRENT_TIMESTAMP),
    actual_end_at = COALESCE(actual_end_at, CURRENT_TIMESTAMP)
WHERE id = %(row_id)s AND session_id = %(session_id)s;
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
