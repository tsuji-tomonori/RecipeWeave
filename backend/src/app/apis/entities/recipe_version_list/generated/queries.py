# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    after_id: UUID | None
    page_limit: int


SQL = """-- レシピ内容版を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.recipe_id,
    t.version,
    t.release_id,
    t.base_servings,
    t.output_amount,
    t.output_unit_id,
    t.status,
    t.validation,
    t.content_hash,
    t.published_at,
    t.description,
    t.xmin::TEXT AS etag
FROM recipeweave.recipe_version AS t
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
