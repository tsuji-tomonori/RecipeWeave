# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 4b1ced2272ecb5a40179c943f7faa1669eaaafd5b8e571c54e9684afa106a3fc
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 現ワーカーのフェンスを確認し、範囲内の単調な進捗だけを確定する。
UPDATE recipeweave.generation_shard AS s
SET next_ordinal = %(next_ordinal)s, state = %(state)s
WHERE
    s.id = %(row_id)s AND s.lease_owner = %(lease_owner)s
    AND s.fence_token = %(expected_fence)s AND s.lease_expires_at > NOW()
    AND s.state = 'running' AND %(next_ordinal)s >= s.next_ordinal
    AND %(next_ordinal)s <= s.end_ordinal
    AND (%(state)s <> 'done' OR %(next_ordinal)s = s.end_ordinal)
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
    "query": ("expected_fence", "lease_owner", "next_ordinal", "row_id", "state")
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
