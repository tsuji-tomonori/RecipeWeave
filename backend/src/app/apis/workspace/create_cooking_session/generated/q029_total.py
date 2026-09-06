# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 28975352341b96bb0f5591d63b55e5388f7504c0bb240c332288a03f3dcb2c97
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 同じ商品・形態・単位の確定需要を一つに合計する。
INSERT INTO recipeweave.ingredient_total
(
    id,
    session_id,
    form_id,
    product_version_id,
    unit_id,
    required_amount,
    quality,
    calculation_version
)
VALUES (
    %(row_id)s,
    %(session_id)s,
    %(form_id)s,
    %(product_id)s,
    %(unit_id)s,
    %(amount)s,
    'reference',
    'decimal-v1'
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("amount", "form_id", "product_id", "row_id", "session_id", "unit_id")
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
