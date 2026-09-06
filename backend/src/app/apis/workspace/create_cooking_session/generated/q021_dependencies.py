# app-docs による自動生成。直接編集しない。
# SQLのSHA256: a98e864a40b465f7c483f5bd5b2bfbda8869ee588a307027b5e0f04f1460bba9
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 同一料理版の材料・品質・安全上の先行条件を読む。
SELECT
    mi.id AS item_id,
    d.before_step_id,
    d.after_step_id,
    d.min_lag_s,
    d.max_lag_s,
    d.kind
FROM recipeweave.menu_item AS mi
INNER JOIN recipeweave.recipe_step AS st ON mi.recipe_version_id = st.recipe_version_id
INNER JOIN recipeweave.step_dependency AS d ON st.id = d.after_step_id
WHERE mi.menu_id = %(menu_id)s
ORDER BY mi.position, d.id;
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
