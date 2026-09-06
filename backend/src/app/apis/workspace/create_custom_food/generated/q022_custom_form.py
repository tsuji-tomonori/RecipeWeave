# app-docs による自動生成。直接編集しない。
# SQLのSHA256: e08c14361eb8db7f62f72fdfd5633effb6e46ab927ace6baa647db75ab02b47e
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 独自食材にも標準形態と基準単位を用意する。
INSERT INTO recipeweave.food_form (id, food_id, name, state, base_unit_id, quantity_basis, status)
SELECT
    %(row_id)s,
    %(food_id)s,
    '標準',
    'raw',
    u.id,
    'as_purchased',
    'active'
FROM recipeweave.unit AS u
WHERE u.code = %(unit)s AND u.status = 'active' RETURNING id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("food_id", "row_id", "unit")}


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
