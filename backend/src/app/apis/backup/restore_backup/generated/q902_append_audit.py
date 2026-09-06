# app-docs による自動生成。直接編集しない。
# SQLのSHA256: e585649a91c22f7a5f9004996ebce89f3c27b4f55be635e6bd022f1013c5dcf4
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 復元本文を複製せず、全置換した本人キーのハッシュだけを監査へ残す。
INSERT INTO recipeweave.audit_event
(id, actor_id, action, entity_type, entity_key_hash, reason, occurred_at)
VALUES (
    %(row_id)s, %(actor_id)s, 'backup/restore', 'workspace', %(key_hash)s,
    '本人が確認した全置換復元', CURRENT_TIMESTAMP
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("actor_id", "key_hash", "row_id")}


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
