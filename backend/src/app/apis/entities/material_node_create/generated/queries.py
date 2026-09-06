# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    amount: Decimal | None
    ingredient_line_id: UUID | None
    kind: str
    name: str
    producer_step_id: UUID | None
    recipe_version_id: UUID
    row_id: UUID
    unit_id: UUID | None


SQL = """-- 材料・中間物節点を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.material_node AS t (
    id,
    recipe_version_id,
    name,
    kind,
    ingredient_line_id,
    producer_step_id,
    amount,
    unit_id
)
VALUES (
    %(row_id)s,
    %(recipe_version_id)s,
    %(name)s,
    %(kind)s,
    %(ingredient_line_id)s,
    %(producer_step_id)s,
    %(amount)s,
    %(unit_id)s
)
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
        "ingredient_line_id": values["ingredient_line_id"],
        "kind": values["kind"],
        "name": values["name"],
        "producer_step_id": values["producer_step_id"],
        "recipe_version_id": values["recipe_version_id"],
        "row_id": values["row_id"],
        "unit_id": values["unit_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
