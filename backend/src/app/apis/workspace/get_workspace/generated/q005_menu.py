# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 52c30cf9391c0a045fd22e0dee8918ae68770ff78895f3a7be1e3de85e6e4cd9
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 現在の献立を固定した本人用IDで読む。
SELECT
    mi.id,
    rv.recipe_id,
    mi.servings,
    mi.recipe_version_id,
    m.revision
FROM recipeweave.menu AS m INNER JOIN recipeweave.menu_item AS mi ON m.id = mi.menu_id
INNER JOIN recipeweave.recipe_version AS rv ON mi.recipe_version_id = rv.id
WHERE m.id = %(menu_id)s AND m.user_id = %(user_id)s
ORDER BY mi.position, mi.id;
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
