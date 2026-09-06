# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 9b55454a113b56fb956a0957c1b547f3ab6baa2a27559509c164d584ec2ae4cc
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 在庫本体・登録時の値・食材形態・単位を別々の正規化行から復元する。
SELECT
    p.id,
    f.food_id,
    f.name AS form,
    p.amount,
    u.code AS unit,
    p.original_amount,
    p.location,
    p.priority,
    p.expires_on,
    p.created_at,
    p.updated_at,
    p.source_import_id,
    p.status,
    p.edited,
    COALESCE(ofm.food_id, f.food_id) AS original_food_id,
    COALESCE(ou.code, u.code) AS original_unit
FROM recipeweave.pantry_lot AS p
INNER JOIN recipeweave.food_form AS f ON p.form_id = f.id
INNER JOIN recipeweave.unit AS u ON p.unit_id = u.id
LEFT JOIN recipeweave.food_form AS ofm ON p.original_form_id = ofm.id
LEFT JOIN recipeweave.unit AS ou ON p.original_unit_id = ou.id
WHERE p.user_id = %(user_id)s
ORDER BY p.created_at, p.id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("user_id",)}


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
