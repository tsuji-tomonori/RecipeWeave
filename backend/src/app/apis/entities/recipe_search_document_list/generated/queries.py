# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    after_id: UUID | None
    page_limit: int


SQL = """-- 公開検索用文書を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.recipe_id,
    t.published_version_id,
    t.projection_version,
    t.display_title,
    t.food_identity_ids,
    t.facet_option_ids,
    t.search_text,
    t.eligible,
    t.source_hash,
    t.projected_at,
    t.xmin::TEXT AS etag
FROM recipeweave.recipe_search_document AS t
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
