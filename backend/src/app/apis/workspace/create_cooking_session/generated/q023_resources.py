# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 60dfff0563457c003fc06f4e425f889644c6db1cea8fe9884a8f610be0e140cf
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 本人が登録した実際の設備数と容量を読む。
SELECT
    k.id,
    k.resource_type_id,
    k.name,
    k.quantity,
    k.capacity,
    rt.code
FROM recipeweave.kitchen_resource AS k
INNER JOIN recipeweave.resource_type AS rt ON k.resource_type_id = rt.id
WHERE k.user_id = %(user_id)s AND k.active
ORDER BY rt.code, k.id;
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
