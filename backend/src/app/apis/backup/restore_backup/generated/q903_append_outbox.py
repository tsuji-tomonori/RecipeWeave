# app-docs による自動生成。直接編集しない。
# SQLのSHA256: f36d4334935d2601817088aadec9cd24c73302016072ee5f99afe6934952b1e9
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 復元完了の本人IDと更新版だけをoutboxへ記録する。
INSERT INTO recipeweave.outbox_event
(id, event_type, aggregate_id, payload, attempt_count)
VALUES (
    %(event_id)s, 'workspace.restored', %(actor_id)s,
    JSONB_BUILD_OBJECT(
        'schema_version', 1, 'event_id', %(event_id)s::TEXT,
        'aggregate_id', %(actor_id)s::TEXT, 'version', %(version)s::BIGINT
    ),
    0
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("actor_id", "event_id", "version")}


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
