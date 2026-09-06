# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 6398d7736ad91430d3fc169cb2daefe6f5d437382e5e7303f59a07db6a69ba57
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの形態・商品別栄養値を元IDと全列で復元する。
INSERT INTO recipeweave.nutrition_fact (
    id,
    created_at,
    form_id,
    product_version_id,
    nutrient_id,
    amount,
    basis_amount,
    basis_unit_id,
    source_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(form_id)s,
    %(product_version_id)s,
    %(nutrient_id)s,
    %(amount)s,
    %(basis_amount)s,
    %(basis_unit_id)s,
    %(source_id)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "amount",
        "basis_amount",
        "basis_unit_id",
        "created_at",
        "form_id",
        "id",
        "nutrient_id",
        "product_version_id",
        "source_id",
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
