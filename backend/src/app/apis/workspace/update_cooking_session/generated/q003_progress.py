# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 838010cb9e29f5f2c6de040b0749549efe068917c2cabd30f442ffba76db9aac
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 完了済み工程の巻戻しをせず進行位置と状態を更新する。
UPDATE recipeweave.cooking_session SET status = %(status)s, current_task_index = %(index)s
WHERE
    id = %(session_id)s AND status IN ('cooking', 'paused')
    AND EXISTS (
        SELECT 1 FROM recipeweave.menu AS m
        WHERE m.id = cooking_session.menu_id AND m.user_id = %(user_id)s
    )
RETURNING id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("index", "session_id", "status", "user_id")}


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
