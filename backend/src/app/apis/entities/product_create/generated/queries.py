# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    brand: str
    food_id: UUID
    gtin: str | None
    name: str
    row_id: UUID
    status: str


SQL = """-- 市販商品識別を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.product AS t (
    id,
    food_id,
    brand,
    name,
    gtin,
    status
)
VALUES (
    %(row_id)s,
    %(food_id)s,
    %(brand)s,
    %(name)s,
    %(gtin)s,
    %(status)s
)
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
        "food_id": values["food_id"],
        "gtin": values["gtin"],
        "name": values["name"],
        "row_id": values["row_id"],
        "status": values["status"],
    }
    return list(connection.execute(SQL, params).fetchall())
