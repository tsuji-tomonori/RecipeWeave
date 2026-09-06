# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 46088b79a4e709dbf275e29a103efeb64e6f2938524c5d2ae917c9c9cbaf0012
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 除外する食品を明示して保存する。
INSERT INTO recipeweave.user_exclusion (id, user_id, food_id, allergen_id, strict)
VALUES (%(row_id)s, %(user_id)s, %(food_id)s, NULL, TRUE);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("food_id", "row_id", "user_id")}


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
