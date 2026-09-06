# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 6a37ae98b3d2041c798252d6351ec54df603756d2b5b65ed1e4826fe3b21c25a
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 再送キーと登録時刻を一度だけ確定する。画像本文は保持しない。
INSERT INTO recipeweave.receipt_import (
    id, user_id, file_sha256, idempotency_key, status, committed_at
)
VALUES (%(import_id)s, %(user_id)s, %(hash)s, %(key)s, 'committed', CURRENT_TIMESTAMP);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("hash", "import_id", "key", "user_id")}


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
