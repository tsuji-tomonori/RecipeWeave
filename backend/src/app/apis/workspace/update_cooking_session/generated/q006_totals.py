# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 664f398c861b8933385571c0f05823a4cb2fee31db3dccd0d7c329dc1453666f
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 消費する量の正本はクライアントの適用結果でなくDBの需要行とする。
SELECT
    t.id,
    t.form_id,
    t.product_version_id,
    t.unit_id,
    t.required_amount,
    fm.food_id,
    fm.name AS form,
    u.code AS unit
FROM recipeweave.ingredient_total AS t INNER JOIN recipeweave.food_form AS fm ON t.form_id = fm.id
INNER JOIN recipeweave.unit AS u ON t.unit_id = u.id
WHERE t.session_id = %(session_id)s
ORDER BY t.id;
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
