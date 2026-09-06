# app-docs による自動生成。直接編集しない。
# SQLのSHA256: cfc6818fceac6db3aff49e4b81f3f443a85249cf507e827524887f4bdbbc32f8
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証した本文と現在版を15分間の最終確認へ結び付ける。
INSERT INTO recipeweave.backup_restore_intent
(id, user_id, artifact_id, body_sha256, current_revision, expires_at)
VALUES (
    %(intent_id)s, %(actor_id)s, %(artifact_id)s, %(body_sha256)s,
    %(current_revision)s, CURRENT_TIMESTAMP + INTERVAL '15 minutes'
)
RETURNING id, expires_at;
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
