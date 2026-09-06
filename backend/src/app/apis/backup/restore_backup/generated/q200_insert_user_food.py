# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 413e056710325779644f9b82157b7b360fef45939c93d075f6049c41645d9d1f
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの利用者が追加した独自食材の所有を元IDと全列で復元する。
INSERT INTO recipeweave.user_food (
    id,
    created_at,
    user_id,
    food_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(food_id)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("created_at", "food_id", "id", "user_id")}


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
