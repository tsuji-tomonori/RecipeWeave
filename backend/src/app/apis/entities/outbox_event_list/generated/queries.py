# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    after_id: UUID | None
    page_limit: int


SQL = """-- 検索・キャッシュ更新配信を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.event_type,
    t.aggregate_id,
    t.payload,
    t.delivered_at,
    t.attempt_count,
    t.xmin::TEXT AS etag
FROM recipeweave.outbox_event AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {"after_id": values["after_id"], "page_limit": values["page_limit"]}
    return list(connection.execute(SQL, params).fetchall())
