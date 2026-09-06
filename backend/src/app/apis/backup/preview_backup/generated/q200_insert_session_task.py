# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 4e2e98a536c6b1959811ecbd84ab08125f90567355826ad1ea275e508c19ea2f
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの展開済み工程を元IDと全列で復元する。
INSERT INTO recipeweave.session_task (
    id,
    created_at,
    session_id,
    menu_item_id,
    step_id,
    batch_no,
    planned_start_s,
    planned_end_s,
    status,
    actual_start_at,
    actual_end_at,
    timer_started_at,
    timer_duration_s,
    duration_source,
    confirmed_duration_s
) VALUES (
    %(id)s,
    %(created_at)s,
    %(session_id)s,
    %(menu_item_id)s,
    %(step_id)s,
    %(batch_no)s,
    %(planned_start_s)s,
    %(planned_end_s)s,
    %(status)s,
    %(actual_start_at)s,
    %(actual_end_at)s,
    %(timer_started_at)s,
    %(timer_duration_s)s,
    %(duration_source)s,
    %(confirmed_duration_s)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "actual_end_at",
        "actual_start_at",
        "batch_no",
        "confirmed_duration_s",
        "created_at",
        "duration_source",
        "id",
        "menu_item_id",
        "planned_end_s",
        "planned_start_s",
        "session_id",
        "status",
        "step_id",
        "timer_duration_s",
        "timer_started_at",
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
