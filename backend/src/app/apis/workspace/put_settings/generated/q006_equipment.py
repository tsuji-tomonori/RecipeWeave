# app-docs による自動生成。直接編集しない。
# SQLのSHA256: c041920b60e405e1f7db38dffe9b06bf4babedda27532c75a9b07b92a4f2296d
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 同じ器具の既存ID・容量を維持して再有効化し、未登録時だけ追加する。
WITH enabled AS (
UPDATE recipeweave.kitchen_resource AS k SET active = TRUE
FROM recipeweave.resource_type AS r WHERE k.user_id = %(user_id)s
AND k.resource_type_id = r.id AND r.name = %(name)s AND r.status = 'active' RETURNING k.id
), inserted AS (
INSERT INTO recipeweave.kitchen_resource (id, user_id, resource_type_id, name, capacity, quantity, active)
SELECT %(row_id)s, %(user_id)s, r.id, r.name, NULL, 1, TRUE FROM recipeweave.resource_type AS r
WHERE r.name = %(name)s AND r.status = 'active' AND NOT EXISTS (SELECT 1 FROM enabled) RETURNING id
) SELECT id FROM enabled UNION ALL SELECT id FROM inserted;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("name", "row_id", "user_id")}


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
