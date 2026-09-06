# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    amount: Decimal | None
    expected_etag: str
    ingredient_line_id: UUID | None
    kind: str
    name: str
    producer_step_id: UUID | None
    recipe_version_id: UUID
    row_id: UUID
    unit_id: UUID | None


SQL = """-- 材料・中間物節点を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.material_node AS t
SET
    recipe_version_id = %(recipe_version_id)s,
    name = %(name)s,
    kind = %(kind)s,
    ingredient_line_id = %(ingredient_line_id)s,
    producer_step_id = %(producer_step_id)s,
    amount = %(amount)s,
    unit_id = %(unit_id)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.name,
    t.kind,
    t.ingredient_line_id,
    t.producer_step_id,
    t.amount,
    t.unit_id,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "amount": values["amount"],
        "expected_etag": values["expected_etag"],
        "ingredient_line_id": values["ingredient_line_id"],
        "kind": values["kind"],
        "name": values["name"],
        "producer_step_id": values["producer_step_id"],
        "recipe_version_id": values["recipe_version_id"],
        "row_id": values["row_id"],
        "unit_id": values["unit_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
