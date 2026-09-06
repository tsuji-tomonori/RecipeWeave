# app-docs による自動生成。直接編集しない。
# SQLのSHA256: a6401ae24ce5731ec3a300aea0cf714428d289d2da7b7b2d9b3b22e1ea6097fe
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 画像と購入品構成の重複を本人の履歴だけで検出する。
SELECT
    id,
    status
FROM recipeweave.receipt_import
WHERE
    user_id = %(user_id)s
    AND (id = %(import_id)s OR file_sha256 = %(hash)s OR idempotency_key LIKE %(signature)s)
ORDER BY created_at;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("hash", "import_id", "signature", "user_id")}


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
