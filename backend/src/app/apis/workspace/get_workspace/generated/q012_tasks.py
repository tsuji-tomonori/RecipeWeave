# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 0f474bd79716f319c05be3e7288aa47617d77065fa55e33465a2a13d3b92f718
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 調理工程とタイマーを正規化されたタスクから読む。
SELECT
    t.id,
    t.menu_item_id,
    t.step_id,
    t.planned_start_s,
    t.planned_end_s,
    t.duration_source,
    t.confirmed_duration_s,
    t.status,
    t.timer_started_at,
    t.timer_duration_s,
    rv.recipe_id,
    r.title AS recipe_name,
    st.title,
    st.instruction,
    st.attention,
    st.duration_max_s,
    scaling.mode AS scaling_mode
FROM recipeweave.session_task AS t INNER JOIN recipeweave.menu_item AS mi ON t.menu_item_id = mi.id
INNER JOIN recipeweave.recipe_version AS rv ON mi.recipe_version_id = rv.id
INNER JOIN recipeweave.recipe AS r ON rv.recipe_id = r.id
INNER JOIN recipeweave.recipe_step AS st ON t.step_id = st.id
INNER JOIN recipeweave.scaling_rule AS scaling ON st.scaling_rule_id = scaling.id
WHERE t.session_id = %(session_id)s
ORDER BY t.planned_start_s, mi.position, st.step_no, t.id;
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
