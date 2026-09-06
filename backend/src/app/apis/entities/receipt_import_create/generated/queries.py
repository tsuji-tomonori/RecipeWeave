# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import datetime
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    committed_at: datetime | None
    file_sha256: str | None
    idempotency_key: str
    reverted_at: datetime | None
    revision: int
    row_id: UUID
    status: str
    undo_preserved_count: int
    user_id: UUID


SQL = """-- レシート読取・在庫登録の処理単位を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.receipt_import AS t (
    id,
    user_id,
    file_sha256,
    idempotency_key,
    status,
    revision,
    committed_at,
    reverted_at,
    undo_preserved_count
)
VALUES (
    %(row_id)s,
    %(user_id)s,
    %(file_sha256)s,
    %(idempotency_key)s,
    %(status)s,
    %(revision)s,
    %(committed_at)s,
    %(reverted_at)s,
    %(undo_preserved_count)s
)
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.file_sha256,
    t.idempotency_key,
    t.status,
    t.revision,
    t.committed_at,
    t.reverted_at,
    t.undo_preserved_count,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "committed_at": values["committed_at"],
        "file_sha256": values["file_sha256"],
        "idempotency_key": values["idempotency_key"],
        "reverted_at": values["reverted_at"],
        "revision": values["revision"],
        "row_id": values["row_id"],
        "status": values["status"],
        "undo_preserved_count": values["undo_preserved_count"],
        "user_id": values["user_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
