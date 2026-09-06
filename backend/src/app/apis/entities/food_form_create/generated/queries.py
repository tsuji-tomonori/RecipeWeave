# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    base_unit_id: UUID
    food_id: UUID
    name: str
    quantity_basis: str
    row_id: UUID
    state: str
    status: str


SQL = """-- 食材形態を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.food_form AS t (
    id,
    food_id,
    name,
    state,
    base_unit_id,
    quantity_basis,
    status
)
VALUES (
    %(row_id)s,
    %(food_id)s,
    %(name)s,
    %(state)s,
    %(base_unit_id)s,
    %(quantity_basis)s,
    %(status)s
)
RETURNING
    t.id,
    t.created_at,
    t.food_id,
    t.name,
    t.state,
    t.base_unit_id,
    t.quantity_basis,
    t.status,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "base_unit_id": values["base_unit_id"],
        "food_id": values["food_id"],
        "name": values["name"],
        "quantity_basis": values["quantity_basis"],
        "row_id": values["row_id"],
        "state": values["state"],
        "status": values["status"],
    }
    return list(connection.execute(SQL, params).fetchall())
