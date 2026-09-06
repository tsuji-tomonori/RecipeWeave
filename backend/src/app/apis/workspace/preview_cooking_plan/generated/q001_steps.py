# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 6cbc70cf6c65d289fd016ea19d28363a3cfe62865fdd9f298dc4f51d32a0a8ea
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 指定料理版の工程を要求の献立行IDへ対応させる。永続行は作成しない。
SELECT
    %(item_id)s::UUID AS item_id,
    %(position)s::INTEGER AS position,
    %(servings)s::NUMERIC AS servings,
    rv.base_servings,
    rv.recipe_id,
    st.id AS step_id,
    st.step_no,
    st.duration_max_s,
    st.attention,
    sc.mode AS scaling_mode,
    sc.batch_capacity,
    sc.min_servings,
    sc.max_servings
FROM recipeweave.recipe_version AS rv
INNER JOIN recipeweave.recipe_step AS st ON rv.id = st.recipe_version_id
INNER JOIN recipeweave.scaling_rule AS sc ON st.scaling_rule_id = sc.id
WHERE rv.id = %(version_id)s
ORDER BY st.step_no;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("item_id", "position", "servings", "version_id")
}


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
