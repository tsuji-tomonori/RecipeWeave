# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 31dd774173a6d37241c56c29f6efcce28a76552c7fe4b9fed122483d17590b35
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 共通の公開版と分離し、本人が編集する私有カタログを初回だけ用意する。
INSERT INTO recipeweave.catalog_release (id, version, manifest_hash, published_at, owner_id)
VALUES (%(release_id)s, %(version)s, %(manifest)s, NULL, %(user_id)s) ON CONFLICT (id) DO NOTHING;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("manifest", "release_id", "user_id", "version")}


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
