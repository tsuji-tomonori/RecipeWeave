# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 4e2f2bfb2fc095626d1c50bd7de2f7be5cb8ec3ed0a3bfe059b4703b961ea126
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 本人・本文・版が一致する未使用かつ期限内の確認をロックする。
SELECT id FROM recipeweave.backup_restore_intent
WHERE
    id = %(intent_id)s AND user_id = %(actor_id)s AND artifact_id = %(artifact_id)s
    AND body_sha256 = %(body_sha256)s AND current_revision = %(current_revision)s
    AND consumed_at IS NULL AND expires_at > CLOCK_TIMESTAMP()
FOR UPDATE;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("actor_id", "artifact_id", "body_sha256", "current_revision", "intent_id")
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
