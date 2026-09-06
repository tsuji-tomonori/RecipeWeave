# app-docs による自動生成。直接編集しない。
# SQLのSHA256: c14c25b03bc2b7536163cee280eaf558db834629397ec087671fdeedf13e618f
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 工程が占有する器具数と最小容量を読む。
SELECT
    sr.step_id,
    sr.resource_type_id,
    sr.quantity,
    sr.capacity_min,
    rt.name,
    rt.code
FROM recipeweave.step_resource AS sr
INNER JOIN recipeweave.resource_type AS rt ON sr.resource_type_id = rt.id
WHERE
    EXISTS (
        SELECT 1 FROM recipeweave.recipe_step AS st INNER JOIN recipeweave.menu_item AS mi
            ON st.recipe_version_id = mi.recipe_version_id
        WHERE mi.menu_id = %(menu_id)s AND st.id = sr.step_id
    )
ORDER BY sr.step_id, rt.code;
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
