# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    row_id: UUID


SQL = """-- レシート読取・在庫登録の処理単位を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
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
    t.xmin::TEXT AS etag
FROM recipeweave.receipt_import AS t
WHERE
    t.id = %(row_id)s
    AND t.user_id = %(actor_id)s;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {"actor_id": values["actor_id"], "row_id": values["row_id"]}
    return list(connection.execute(SQL, params).fetchall())
