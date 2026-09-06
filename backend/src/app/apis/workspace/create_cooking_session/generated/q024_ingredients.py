# app-docs による自動生成。直接編集しない。
# SQLのSHA256: f317f8008baab20827a26737068c88e7142daab26a0eb2978daa1c8331d70794
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 分量を食品名でなく形態・単位・商品版ごとに合計する。
SELECT
    ri.id AS ingredient_id,
    ri.form_id,
    ri.product_version_id,
    ri.unit_id,
    ri.conversion_id,
    mi.id AS item_id,
    rv.id AS recipe_version_id,
    mi.servings,
    COALESCE(ov.amount, ri.amount * mi.servings / rv.base_servings) AS amount
FROM recipeweave.menu_item AS mi
INNER JOIN recipeweave.recipe_version AS rv ON mi.recipe_version_id = rv.id
INNER JOIN recipeweave.recipe_ingredient AS ri ON rv.id = ri.recipe_version_id
LEFT JOIN
    recipeweave.menu_ingredient_override AS ov
    ON mi.id = ov.menu_item_id AND ri.id = ov.ingredient_line_id
WHERE
    mi.menu_id = %(menu_id)s AND ri.demand_kind <> 'kit_component'
    AND (NOT ri.optional OR ov.selected)
ORDER BY mi.position, ri.line_no;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("menu_id",)}


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
