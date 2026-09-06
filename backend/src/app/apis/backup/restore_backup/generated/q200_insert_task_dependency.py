# app-docs による自動生成。直接編集しない。
# SQLのSHA256: b43accae305854ac7f73e98129b91f6d9eda58aac7027734b27df2e8eca2ce2e
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの献立展開後依存を元IDと全列で復元する。
INSERT INTO recipeweave.task_dependency (
    id,
    created_at,
    before_task_id,
    after_task_id,
    min_lag_s,
    max_lag_s,
    reason
) VALUES (
    %(id)s,
    %(created_at)s,
    %(before_task_id)s,
    %(after_task_id)s,
    %(min_lag_s)s,
    %(max_lag_s)s,
    %(reason)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "after_task_id",
        "before_task_id",
        "created_at",
        "id",
        "max_lag_s",
        "min_lag_s",
        "reason",
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
