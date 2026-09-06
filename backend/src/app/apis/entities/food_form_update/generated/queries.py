# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    base_unit_id: UUID
    expected_etag: str
    food_id: UUID
    name: str
    quantity_basis: str
    row_id: UUID
    state: str
    status: str


SQL = """-- 食材形態を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.food_form AS t
SET
    food_id = %(food_id)s,
    name = %(name)s,
    state = %(state)s,
    base_unit_id = %(base_unit_id)s,
    quantity_basis = %(quantity_basis)s,
    status = %(status)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
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
        "expected_etag": values["expected_etag"],
        "food_id": values["food_id"],
        "name": values["name"],
        "quantity_basis": values["quantity_basis"],
        "row_id": values["row_id"],
        "state": values["state"],
        "status": values["status"],
    }
    return list(connection.execute(SQL, params).fetchall())
