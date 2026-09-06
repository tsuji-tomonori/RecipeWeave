# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 1917adb8a95a88eac63653140294a92e33ab1099358814644f1ceb514e9a4730
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 調理計画が参照する献立版を更新する。
UPDATE recipeweave.menu SET revision = revision + 1
WHERE id = %(menu_id)s AND user_id = %(user_id)s RETURNING revision;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("menu_id", "user_id")}


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
