# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    base_servings: Decimal
    content_hash: str
    description: str | None
    output_amount: Decimal
    output_unit_id: UUID
    published_at: datetime | None
    recipe_id: UUID
    release_id: UUID
    row_id: UUID
    status: str
    validation: str
    version: int


SQL = """-- レシピ内容版を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.recipe_version AS t (
    id,
    recipe_id,
    version,
    release_id,
    base_servings,
    output_amount,
    output_unit_id,
    status,
    validation,
    content_hash,
    published_at,
    description
)
VALUES (
    %(row_id)s,
    %(recipe_id)s,
    %(version)s,
    %(release_id)s,
    %(base_servings)s,
    %(output_amount)s,
    %(output_unit_id)s,
    %(status)s,
    %(validation)s,
    %(content_hash)s,
    %(published_at)s,
    %(description)s
)
RETURNING
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
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "base_servings": values["base_servings"],
        "content_hash": values["content_hash"],
        "description": values["description"],
        "output_amount": values["output_amount"],
        "output_unit_id": values["output_unit_id"],
        "published_at": values["published_at"],
        "recipe_id": values["recipe_id"],
        "release_id": values["release_id"],
        "row_id": values["row_id"],
        "status": values["status"],
        "validation": values["validation"],
        "version": values["version"],
    }
    return list(connection.execute(SQL, params).fetchall())
