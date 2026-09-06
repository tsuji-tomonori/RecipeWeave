# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    row_id: UUID


SQL = """-- 公開検索用文書を取得する。
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
    t.id = %(row_id)s
    AND TRUE;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {"row_id": values["row_id"]}
    return list(connection.execute(SQL, params).fetchall())
