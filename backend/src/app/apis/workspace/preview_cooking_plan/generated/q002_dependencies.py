# app-docs による自動生成。直接編集しない。
# SQLのSHA256: c2c8ab551635ef2b559ac4971956800919e9dcf5924d17205ffaa53586104533
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 指定料理版の安全・材料・品質に基づく先行条件を読む。
SELECT
    %(item_id)s::UUID AS item_id,
    d.before_step_id,
    d.after_step_id,
    d.min_lag_s,
    d.max_lag_s,
    d.kind
FROM recipeweave.recipe_step AS st
INNER JOIN recipeweave.step_dependency AS d ON st.id = d.after_step_id
WHERE st.recipe_version_id = %(version_id)s
ORDER BY d.id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("item_id", "version_id")}


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
