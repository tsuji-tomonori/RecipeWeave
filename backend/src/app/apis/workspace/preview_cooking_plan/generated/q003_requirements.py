# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 5fc4046c89f9c1f496de07207a322e5a0fb332e1ec2ce9cf8ec265dced7a96dc
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 工程が必要とする器具の台数と単位容量を読む。
SELECT
    sr.step_id,
    sr.resource_type_id,
    sr.quantity,
    sr.capacity_min,
    sr.exclusive,
    rt.name,
    rt.code
FROM recipeweave.step_resource AS sr
INNER JOIN recipeweave.recipe_step AS st ON sr.step_id = st.id
INNER JOIN recipeweave.resource_type AS rt ON sr.resource_type_id = rt.id
WHERE st.recipe_version_id = %(version_id)s
ORDER BY sr.step_id, rt.code;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("version_id",)}


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
