# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 5e8414ff1cb91fb1c7db95680a1f920839ebf34899635c4e13190259ecb245ef
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの商品表示アレルゲンを元IDと全列で復元する。
INSERT INTO recipeweave.product_allergen (
    id,
    created_at,
    product_version_id,
    allergen_id,
    presence,
    source_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(product_version_id)s,
    %(allergen_id)s,
    %(presence)s,
    %(source_id)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("allergen_id", "created_at", "id", "presence", "product_version_id", "source_id")
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
