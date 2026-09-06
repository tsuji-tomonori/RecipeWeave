# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    capacity: Decimal | None
    name: str
    quantity: int
    resource_type_id: UUID
    row_id: UUID
    user_id: UUID


SQL = """-- キッチンの実資源を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.kitchen_resource AS t (
    id,
    user_id,
    resource_type_id,
    name,
    capacity,
    quantity
)
VALUES (
    %(row_id)s,
    %(user_id)s,
    %(resource_type_id)s,
    %(name)s,
    %(capacity)s,
    %(quantity)s
)
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.resource_type_id,
    t.name,
    t.capacity,
    t.quantity,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "capacity": values["capacity"],
        "name": values["name"],
        "quantity": values["quantity"],
        "resource_type_id": values["resource_type_id"],
        "row_id": values["row_id"],
        "user_id": values["user_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
