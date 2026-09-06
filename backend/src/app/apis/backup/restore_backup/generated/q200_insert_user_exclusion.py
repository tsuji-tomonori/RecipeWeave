# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 10cd7434d6262ef711c0019f6a13f6b02e944d0de5d04bbe4455ebfd1bc2a7cc
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの避けたい食材・物質を元IDと全列で復元する。
INSERT INTO recipeweave.user_exclusion (
    id,
    created_at,
    user_id,
    food_id,
    allergen_id,
    strict
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(food_id)s,
    %(allergen_id)s,
    %(strict)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("allergen_id", "created_at", "food_id", "id", "strict", "user_id")
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
