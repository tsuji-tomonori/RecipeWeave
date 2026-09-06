# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    alias: str
    expected_etag: str
    food_id: UUID
    locale: str
    row_id: UUID


SQL = """-- 食材別名を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.food_alias AS t
SET
    food_id = %(food_id)s,
    alias = %(alias)s,
    locale = %(locale)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.food_id,
    t.alias,
    t.locale,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "alias": values["alias"],
        "expected_etag": values["expected_etag"],
        "food_id": values["food_id"],
        "locale": values["locale"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
