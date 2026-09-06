# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    brand: str
    expected_etag: str
    food_id: UUID
    gtin: str | None
    name: str
    row_id: UUID
    status: str


SQL = """-- 市販商品識別を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.product AS t
SET
    food_id = %(food_id)s,
    brand = %(brand)s,
    name = %(name)s,
    gtin = %(gtin)s,
    status = %(status)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.food_id,
    t.brand,
    t.name,
    t.gtin,
    t.status,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "brand": values["brand"],
        "expected_etag": values["expected_etag"],
        "food_id": values["food_id"],
        "gtin": values["gtin"],
        "name": values["name"],
        "row_id": values["row_id"],
        "status": values["status"],
    }
    return list(connection.execute(SQL, params).fetchall())
