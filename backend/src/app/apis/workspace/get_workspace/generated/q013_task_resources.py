# app-docs による自動生成。直接編集しない。
# SQLのSHA256: f6ed366fa2ff15dd7147993529dec399ed1a7defe21a012681df4966070026a7
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- タスクに必要な器具の表示名を読む。
SELECT
    t.id AS task_id,
    r.name
FROM recipeweave.session_task AS t
INNER JOIN recipeweave.step_resource AS sr ON t.step_id = sr.step_id
INNER JOIN recipeweave.resource_type AS r ON sr.resource_type_id = r.id
WHERE t.session_id = %(session_id)s AND r.code <> 'person'
ORDER BY t.id, r.name;
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
