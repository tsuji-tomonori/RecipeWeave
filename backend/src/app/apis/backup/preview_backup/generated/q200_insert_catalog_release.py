# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 1f5222a09e4a70b71a23b52c188a945e254db08e50c417de076c8a4bcd8cdfe1
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップのカタログ公開版を元IDと全列で復元する。
INSERT INTO recipeweave.catalog_release (
    id,
    created_at,
    version,
    manifest_hash,
    published_at,
    owner_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(version)s,
    %(manifest_hash)s,
    %(published_at)s,
    %(owner_id)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("created_at", "id", "manifest_hash", "owner_id", "published_at", "version")
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
