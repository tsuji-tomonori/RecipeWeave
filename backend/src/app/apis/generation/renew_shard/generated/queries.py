# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 4d26a593cbe54b19e502877ce997c2603bdf52c84155d09019b7ad9520633628
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "001_execute": """\
-- 本人・フェンス・有効期限が一致する現ワーカーだけがリースを延長する。
UPDATE recipeweave.generation_shard AS s
SET lease_expires_at = NOW() + MAKE_INTERVAL(secs => %(lease_seconds)s)
WHERE
    s.id = %(row_id)s AND s.lease_owner = %(lease_owner)s
    AND s.fence_token = %(expected_fence)s AND s.lease_expires_at > NOW()
    AND s.state = 'running'
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
PARAMETERS: dict[str, tuple[str, ...]] = {
    "001_execute": ("expected_fence", "lease_owner", "lease_seconds", "row_id")
}


def execute(
    connection: Connection[dict[str, Any]], name: str, params: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """許可された固定SQLだけに、宣言と一致する束縛値を別渡しする。"""
    if name not in QUERIES or set(params) != set(PARAMETERS[name]):
        raise ValueError("SQL名または束縛パラメータが操作契約にありません")
    cursor = connection.execute(QUERIES[name], dict(params))
    return list(cursor.fetchall()) if cursor.description is not None else []
