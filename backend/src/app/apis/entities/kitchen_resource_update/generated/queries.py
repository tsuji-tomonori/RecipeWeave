# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    active: bool
    actor_id: UUID
    capacity: Decimal | None
    expected_etag: str
    name: str
    quantity: int
    resource_type_id: UUID
    row_id: UUID
    user_id: UUID


SQL = """-- キッチンの実資源を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.kitchen_resource AS t
SET
    user_id = %(user_id)s,
    resource_type_id = %(resource_type_id)s,
    name = %(name)s,
    capacity = %(capacity)s,
    quantity = %(quantity)s,
    active = %(active)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND t.user_id = %(actor_id)s
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.resource_type_id,
    t.name,
    t.capacity,
    t.quantity,
    t.active,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "active": values["active"],
        "actor_id": values["actor_id"],
        "capacity": values["capacity"],
        "expected_etag": values["expected_etag"],
        "name": values["name"],
        "quantity": values["quantity"],
        "resource_type_id": values["resource_type_id"],
        "row_id": values["row_id"],
        "user_id": values["user_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
