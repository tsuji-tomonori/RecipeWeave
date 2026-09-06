# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 8528c1829f25064d89f9dbe2bc6684bed3678504a9c06afb4d5f876fa101417e
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 使用量の結果は合計表と消費台帳から導出する。
SELECT
    total.id,
    fm.food_id,
    fm.name AS form,
    total.required_amount,
    total.actual_amount,
    total.consumption_outcome,
    u.code AS unit,
    COALESCE(SUM(c.amount), 0) AS consumed_amount,
    ARRAY_AGG(c.lot_id) FILTER (WHERE c.id IS NOT NULL) AS lot_ids
FROM recipeweave.ingredient_total AS total
INNER JOIN recipeweave.food_form AS fm ON total.form_id = fm.id
INNER JOIN recipeweave.unit AS u ON total.unit_id = u.id
LEFT JOIN recipeweave.pantry_lot AS p
    ON
        total.form_id = p.form_id AND total.unit_id = p.unit_id
        AND total.product_version_id IS NOT DISTINCT FROM p.product_version_id
LEFT JOIN recipeweave.pantry_consumption AS c ON p.id = c.lot_id AND total.session_id = c.session_id
WHERE total.session_id = %(session_id)s
GROUP BY total.id, fm.food_id, fm.name, u.code
ORDER BY total.id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("session_id",)}


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
