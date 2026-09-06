# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 894fd27b91abcb09c82cf27f83fd87da02533d77172912c24cca4755b5430cc0
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 公開済み料理、または明示したローカル試用で利用できる料理版を選ぶ。
SELECT
    rv.id,
    rv.base_servings
FROM recipeweave.recipe_version AS rv
INNER JOIN
    recipeweave.recipe AS r
    ON rv.recipe_id = r.id
WHERE
    r.id = %(recipe_id)s
    AND (%(requested_version_id)s::UUID IS NULL OR rv.id = %(requested_version_id)s)
    AND (
        (rv.status = 'published' AND rv.validation = 'passed' AND r.status = 'published')
        OR (%(preview)s AND rv.status = 'draft' AND r.status = 'draft')
    )
ORDER BY rv.version DESC
LIMIT 1;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("preview", "recipe_id", "requested_version_id")}


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
