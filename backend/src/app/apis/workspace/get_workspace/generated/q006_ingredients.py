# app-docs による自動生成。直接編集しない。
# SQLのSHA256: a633521b37e30c375781beb47144a4fa9a8d201749719dcdd837a1d04fc4107f
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 献立の確定分量を材料行と上書き行から復元する。
SELECT
    mi.id AS menu_item_id,
    f.food_id,
    f.name AS form,
    ri.id AS ingredient_id,
    CASE WHEN ov.selected = FALSE THEN 0 ELSE ov.amount END AS override_amount,
    u.code AS unit,
    ov.id AS override_id,
    ri.amount * mi.servings / rv.base_servings AS scaled_amount
FROM recipeweave.menu_item AS mi INNER JOIN recipeweave.menu AS m ON mi.menu_id = m.id
INNER JOIN recipeweave.recipe_version AS rv ON mi.recipe_version_id = rv.id
INNER JOIN recipeweave.recipe_ingredient AS ri ON rv.id = ri.recipe_version_id
INNER JOIN recipeweave.food_form AS f ON ri.form_id = f.id
INNER JOIN recipeweave.unit AS u ON ri.unit_id = u.id
LEFT JOIN
    recipeweave.menu_ingredient_override AS ov
    ON mi.id = ov.menu_item_id AND ri.id = ov.ingredient_line_id
WHERE m.id = %(menu_id)s AND m.user_id = %(user_id)s
ORDER BY mi.position, ri.line_no;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("menu_id", "user_id")}


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
