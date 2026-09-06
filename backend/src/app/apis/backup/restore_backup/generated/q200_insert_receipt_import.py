# app-docs による自動生成。直接編集しない。
# SQLのSHA256: d4c8776ffc8a32fe0a45d1bcbfb86f1be69c4ce90f6208731e842c2ee1afd694
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップのレシート読取・在庫登録の処理単位を元IDと全列で復元する。
INSERT INTO recipeweave.receipt_import (
    id,
    created_at,
    user_id,
    file_sha256,
    idempotency_key,
    status,
    revision,
    committed_at,
    reverted_at,
    undo_preserved_count
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(file_sha256)s,
    %(idempotency_key)s,
    %(status)s,
    %(revision)s,
    %(committed_at)s,
    %(reverted_at)s,
    %(undo_preserved_count)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "committed_at",
        "created_at",
        "file_sha256",
        "id",
        "idempotency_key",
        "reverted_at",
        "revision",
        "status",
        "undo_preserved_count",
        "user_id",
    )
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
