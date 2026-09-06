# app-docs による自動生成。直接編集しない。
# SQLのSHA256: dbe6301db87dd66ad68a1fd7e673f43ad5146a44f12cf19c55dfef839ef625b8
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 待機または失効した範囲を排他取得し、新しいフェンスでリースを開始する。
WITH selected AS (
    SELECT id FROM recipeweave.generation_shard
    WHERE
        (state = 'queued' OR (state = 'running' AND lease_expires_at <= NOW()))
        AND (%(template_id)s::UUID IS NULL OR template_id = %(template_id)s)
    ORDER BY created_at, id
    LIMIT 1
    FOR UPDATE SKIP LOCKED
)

UPDATE recipeweave.generation_shard AS s
SET
    lease_owner = %(lease_owner)s,
    lease_expires_at = NOW() + MAKE_INTERVAL(secs => %(lease_seconds)s),
    fence_token = s.fence_token + 1,
    state = 'running'
FROM selected
WHERE s.id = selected.id
RETURNING
    s.id,
    s.created_at,
    s.template_id,
    s.start_ordinal,
    s.end_ordinal,
    s.next_ordinal,
    s.lease_owner,
    s.lease_expires_at,
    s.fence_token,
    s.state,
    s.xmin::TEXT AS etag;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("lease_owner", "lease_seconds", "template_id")}


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
