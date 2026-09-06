# app-docs による自動生成。直接編集しない。
# SQLのSHA256: e5a35d8dc2d7e28f80ccf56043b671d79f700d3176b6e1ef316ebca1183932a1
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの食材形態を元IDと全列で復元する。
INSERT INTO recipeweave.food_form (
    id,
    created_at,
    food_id,
    name,
    state,
    base_unit_id,
    quantity_basis,
    status
) VALUES (
    %(id)s,
    %(created_at)s,
    %(food_id)s,
    %(name)s,
    %(state)s,
    %(base_unit_id)s,
    %(quantity_basis)s,
    %(status)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "base_unit_id",
        "created_at",
        "food_id",
        "id",
        "name",
        "quantity_basis",
        "state",
        "status",
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
