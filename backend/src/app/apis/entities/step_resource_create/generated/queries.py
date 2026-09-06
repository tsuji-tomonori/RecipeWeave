# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    capacity_min: Decimal | None
    exclusive: bool
    quantity: int
    resource_type_id: UUID
    row_id: UUID
    step_id: UUID


SQL = """-- 工程の資源要求を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.step_resource AS t (
    id,
    step_id,
    resource_type_id,
    quantity,
    capacity_min,
    exclusive
)
VALUES (
    %(row_id)s,
    %(step_id)s,
    %(resource_type_id)s,
    %(quantity)s,
    %(capacity_min)s,
    %(exclusive)s
)
RETURNING
    t.id,
    t.created_at,
    t.step_id,
    t.resource_type_id,
    t.quantity,
    t.capacity_min,
    t.exclusive,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "capacity_min": values["capacity_min"],
        "exclusive": values["exclusive"],
        "quantity": values["quantity"],
        "resource_type_id": values["resource_type_id"],
        "row_id": values["row_id"],
        "step_id": values["step_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
