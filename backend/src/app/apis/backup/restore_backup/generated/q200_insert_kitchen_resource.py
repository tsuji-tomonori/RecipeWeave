# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 971bce45db5ac8434c49945e86a9d5b8e3075650f8be49316c8f555f7231b22e
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップのキッチンの実資源を元IDと全列で復元する。
INSERT INTO recipeweave.kitchen_resource (
    id,
    created_at,
    user_id,
    resource_type_id,
    name,
    capacity,
    quantity,
    active
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(resource_type_id)s,
    %(name)s,
    %(capacity)s,
    %(quantity)s,
    %(active)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "active",
        "capacity",
        "created_at",
        "id",
        "name",
        "quantity",
        "resource_type_id",
        "user_id",
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
