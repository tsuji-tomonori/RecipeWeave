# app-docs による自動生成。直接編集しない。
# SQLのSHA256: a82460c8ee631fd6c036207fd13263c4159995cf6dd7501b48a99dc23ccad882
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 最終確認を一度だけ消費し、失敗時には全置換とともに取消す。
UPDATE recipeweave.backup_restore_intent SET consumed_at = CLOCK_TIMESTAMP()
WHERE
    id = %(intent_id)s AND user_id = %(actor_id)s AND body_sha256 = %(body_sha256)s
    AND current_revision = %(current_revision)s AND consumed_at IS NULL
    AND expires_at > CLOCK_TIMESTAMP()
RETURNING id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("actor_id", "body_sha256", "current_revision", "intent_id")
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
