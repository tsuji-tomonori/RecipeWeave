# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 2a9c4834b712d82c0be6e6a1691d26de88903873442aff4a9eecc79a98feee45
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの市販商品識別を元IDと全列で復元する。
INSERT INTO recipeweave.product (
    id,
    created_at,
    food_id,
    brand,
    name,
    gtin,
    status
) VALUES (
    %(id)s,
    %(created_at)s,
    %(food_id)s,
    %(brand)s,
    %(name)s,
    %(gtin)s,
    %(status)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("brand", "created_at", "food_id", "gtin", "id", "name", "status")
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
