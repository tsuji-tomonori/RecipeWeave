# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 1160606c20a352ea612f82bd5701046444d33b128068a450da1c63f983ce396c
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 独自食材の所有者を認証主体へ固定する。
INSERT INTO recipeweave.user_food (id, user_id, food_id) VALUES (
    %(row_id)s, %(user_id)s, %(food_id)s
);
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
