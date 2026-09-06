# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    expected_etag: str
    food_id: UUID
    option_id: UUID
    row_id: UUID


SQL = """-- 食材の分類属性を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.food_axis_option AS t
SET
    food_id = %(food_id)s,
    option_id = %(option_id)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.food_id,
    t.option_id,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "expected_etag": values["expected_etag"],
        "food_id": values["food_id"],
        "option_id": values["option_id"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
