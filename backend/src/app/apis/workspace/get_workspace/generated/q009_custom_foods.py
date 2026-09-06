# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 196765aad339735fda204f4e2c398953a02c3c3d4b0c69d1c0d42f041b8037ca
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 本人の独自食材は所有表を経由して取得する。
SELECT
    f.id,
    f.name,
    u.code AS unit
FROM recipeweave.user_food AS owned
INNER JOIN recipeweave.food AS f ON owned.food_id = f.id
INNER JOIN recipeweave.food_form AS fm ON f.id = fm.food_id
INNER JOIN recipeweave.unit AS u ON fm.base_unit_id = u.id
WHERE owned.user_id = %(user_id)s
ORDER BY f.name, f.id;
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
