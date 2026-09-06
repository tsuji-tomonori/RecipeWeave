# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 5ea2333d0e787a8106b6b2b73835659e3ef6702eeb16d780c8f3b6b758cf33c0
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップのセット内構成品を元IDと全列で復元する。
INSERT INTO recipeweave.product_component (
    id,
    created_at,
    product_version_id,
    form_id,
    name,
    amount,
    unit_id,
    quality
) VALUES (
    %(id)s,
    %(created_at)s,
    %(product_version_id)s,
    %(form_id)s,
    %(name)s,
    %(amount)s,
    %(unit_id)s,
    %(quality)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "amount",
        "created_at",
        "form_id",
        "id",
        "name",
        "product_version_id",
        "quality",
        "unit_id",
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
