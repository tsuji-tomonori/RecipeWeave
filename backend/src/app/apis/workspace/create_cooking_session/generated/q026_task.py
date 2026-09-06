# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 1613d24fee8aa4b61c34dd04ed01cd52b67c1e681eb0f7faa924c3c4cd0aae6c
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 計画済み工程を独立したタスク行へ保存する。
INSERT INTO recipeweave.session_task
(
    id, session_id, menu_item_id, step_id, batch_no, planned_start_s, planned_end_s, status,
    duration_source, confirmed_duration_s
)
VALUES (
    %(row_id)s, %(session_id)s, %(item_id)s, %(step_id)s, 1, %(start)s, %(end)s, 'pending',
    %(duration_source)s, %(confirmed_duration_s)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "confirmed_duration_s",
        "duration_source",
        "end",
        "item_id",
        "row_id",
        "session_id",
        "start",
        "step_id",
    )
}


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
