# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 5f6a0d5ee9343b66bcf51f99482cba62f54230600bc97d0ee86516c3a1ed2f31
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.operation AS t
WHERE t.id = ANY(%(reference_ids)s::UUID[]) AND (TRUE);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("reference_ids",)}


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
