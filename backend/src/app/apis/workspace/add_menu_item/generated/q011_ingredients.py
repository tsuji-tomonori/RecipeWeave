# app-docs による自動生成。直接編集しない。
# SQLのSHA256: ee4943809526a9e373c7a5ea9b82972d10a9d72ba4355711324ea164e422e513
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 指定料理の材料ID・単位・基準量を照合する。
SELECT
    ri.id,
    fm.food_id,
    ri.amount, ri.optional,
    ri.unit_id,
    ri.form_id,
    u.code AS unit
FROM recipeweave.recipe_ingredient AS ri
INNER JOIN recipeweave.food_form AS fm ON ri.form_id = fm.id
INNER JOIN recipeweave.unit AS u ON ri.unit_id = u.id
WHERE ri.recipe_version_id = %(version_id)s
ORDER BY ri.line_no;
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
