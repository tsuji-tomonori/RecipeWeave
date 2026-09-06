# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    allergen_id: UUID
    form_id: UUID
    presence: str
    row_id: UUID
    source_id: UUID


SQL = """-- 食材アレルゲン知識を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.food_allergen AS t (
    id,
    form_id,
    allergen_id,
    presence,
    source_id
)
VALUES (
    %(row_id)s,
    %(form_id)s,
    %(allergen_id)s,
    %(presence)s,
    %(source_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.form_id,
    t.allergen_id,
    t.presence,
    t.source_id,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "allergen_id": values["allergen_id"],
        "form_id": values["form_id"],
        "presence": values["presence"],
        "row_id": values["row_id"],
        "source_id": values["source_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
