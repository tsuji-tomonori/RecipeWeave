# app-docs による自動生成。直接編集しない。
# SQLのSHA256: a24e3bb094def0d08b21aa15e7d2bc71394b01b69ab07b768aba0714c6a08a3a
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの食材の分類属性を元IDと全列で復元する。
INSERT INTO recipeweave.food_axis_option (
    id,
    created_at,
    food_id,
    option_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(food_id)s,
    %(option_id)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("created_at", "food_id", "id", "option_id")}


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
