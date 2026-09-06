# app-docs による自動生成。直接編集しない。
# SQLのSHA256: f163a89a593578147ad30117771d398140af6de98194edc75605b81e1078ff87
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 計画が参照する専用献立の確定版を読む。
SELECT revision FROM recipeweave.menu
WHERE id = %(menu_id)s AND user_id = %(user_id)s;
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
