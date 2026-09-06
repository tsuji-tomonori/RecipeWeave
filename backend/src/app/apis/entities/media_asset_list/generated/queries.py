# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    after_id: UUID | None
    page_limit: int


SQL = """-- 教育用動画等の版を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.operation_id,
    t.media_type,
    t.uri,
    t.sha256,
    t.locale,
    t.version,
    t.parameter_contract,
    t.source_id,
    t.validation,
    t.xmin::TEXT AS etag
FROM recipeweave.media_asset AS t
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
