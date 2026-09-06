# app-docs による自動生成。直接編集しない。
# SQLのSHA256: c23371014c55685a4ce5275660e10eee0df33f669acfb38edbf0d93c3a8215fc
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 同一セッションとロットの二重消費を一意制約で防ぐ。
INSERT INTO recipeweave.pantry_consumption (id, user_id, session_id, lot_id, amount, unit_id)
VALUES (%(row_id)s, %(user_id)s, %(session_id)s, %(lot_id)s, %(amount)s, %(unit_id)s);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("amount", "lot_id", "row_id", "session_id", "unit_id", "user_id")
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
