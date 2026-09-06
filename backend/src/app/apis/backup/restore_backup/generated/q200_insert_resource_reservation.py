# app-docs による自動生成。直接編集しない。
# SQLのSHA256: cb98c239c7b3a3a4489edd1cc187123f1fb331ac7156905a33b291c07586d823
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの資源の予約を元IDと全列で復元する。
INSERT INTO recipeweave.resource_reservation (
    id,
    created_at,
    task_id,
    resource_id,
    start_s,
    end_s,
    quantity
) VALUES (
    %(id)s,
    %(created_at)s,
    %(task_id)s,
    %(resource_id)s,
    %(start_s)s,
    %(end_s)s,
    %(quantity)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("created_at", "end_s", "id", "quantity", "resource_id", "start_s", "task_id")
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
