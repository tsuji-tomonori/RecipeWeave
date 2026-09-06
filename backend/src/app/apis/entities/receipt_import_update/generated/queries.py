# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import datetime
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    committed_at: datetime | None
    expected_etag: str
    file_sha256: str | None
    idempotency_key: str
    reverted_at: datetime | None
    revision: int
    row_id: UUID
    status: str
    user_id: UUID


SQL = """-- レシート読取・在庫登録の処理単位を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.receipt_import AS t
SET
    user_id = %(user_id)s,
    file_sha256 = %(file_sha256)s,
    idempotency_key = %(idempotency_key)s,
    status = %(status)s,
    revision = %(revision)s,
    committed_at = %(committed_at)s,
    reverted_at = %(reverted_at)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND t.user_id = %(actor_id)s
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
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "actor_id": values["actor_id"],
        "committed_at": values["committed_at"],
        "expected_etag": values["expected_etag"],
        "file_sha256": values["file_sha256"],
        "idempotency_key": values["idempotency_key"],
        "reverted_at": values["reverted_at"],
        "revision": values["revision"],
        "row_id": values["row_id"],
        "status": values["status"],
        "user_id": values["user_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
