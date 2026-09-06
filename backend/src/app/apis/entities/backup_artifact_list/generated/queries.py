# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    after_id: UUID | None
    page_limit: int


SQL = """-- 本人へ発行したバックアップの証拠。本文を保存せず、削除後も匿名化した発行記録を保持するを一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.user_id,
    t.body_sha256,
    t.format_version,
    t.xmin::TEXT AS etag
FROM recipeweave.backup_artifact AS t
WHERE
    t.user_id = %(actor_id)s
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "actor_id": values["actor_id"],
        "after_id": values["after_id"],
        "page_limit": values["page_limit"],
    }
    return list(connection.execute(SQL, params).fetchall())
