# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 9a5b175cd62d40357a8777c7315440e24d1a0db95e4413a5be86205bfd00f73c
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 画像本文を保存せず、重複検知と取消しに必要な履歴だけを読む。
SELECT
    r.id,
    r.file_sha256,
    r.idempotency_key,
    r.created_at,
    r.status,
    r.reverted_at
FROM
    recipeweave.receipt_import AS r
WHERE
    r.user_id = %(user_id)s
    AND r.status IN ('committed', 'reverted')
ORDER BY r.created_at, r.id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("user_id",)}


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
