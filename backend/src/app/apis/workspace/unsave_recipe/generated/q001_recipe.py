# app-docs による自動生成。直接編集しない。
# SQLのSHA256: a7b23af452bb18355a2204998fa0223b909442d9d529752935c4935c600dc060
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 公開条件を満たす料理版を保存対象として確認する。
SELECT rv.id
FROM recipeweave.recipe_version AS rv
INNER JOIN recipeweave.recipe AS r ON rv.recipe_id = r.id
WHERE
    r.id = %(recipe_id)s AND (
        (rv.status = 'published' AND r.status = 'published' AND rv.validation = 'passed')
        OR (%(preview)s AND rv.status = 'draft' AND r.status = 'draft')
    )
ORDER BY rv.version DESC LIMIT 1;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("preview", "recipe_id")}


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
