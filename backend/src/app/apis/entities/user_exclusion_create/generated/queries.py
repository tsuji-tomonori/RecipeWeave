# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    allergen_id: UUID | None
    food_id: UUID | None
    row_id: UUID
    strict: bool
    user_id: UUID


SQL = """-- 避けたい食材・物質を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.user_exclusion AS t (
    id,
    user_id,
    food_id,
    allergen_id,
    strict
)
VALUES (
    %(row_id)s,
    %(user_id)s,
    %(food_id)s,
    %(allergen_id)s,
    %(strict)s
)
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.food_id,
    t.allergen_id,
    t.strict,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "allergen_id": values["allergen_id"],
        "food_id": values["food_id"],
        "row_id": values["row_id"],
        "strict": values["strict"],
        "user_id": values["user_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
