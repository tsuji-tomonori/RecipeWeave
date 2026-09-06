# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    amount: Decimal | None
    amount_max: Decimal | None
    amount_mode: str
    canonical_amount: Decimal | None
    component_id: UUID | None
    conversion_id: UUID | None
    demand_kind: str
    expected_etag: str
    form_id: UUID
    kit_parent_line_id: UUID | None
    line_no: int
    note: str | None
    optional: bool
    product_version_id: UUID | None
    recipe_version_id: UUID
    role: str
    row_id: UUID
    scaling_rule_id: UUID
    unit_id: UUID


SQL = """-- レシピ材料明細を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.recipe_ingredient AS t
SET
    recipe_version_id = %(recipe_version_id)s,
    line_no = %(line_no)s,
    form_id = %(form_id)s,
    product_version_id = %(product_version_id)s,
    component_id = %(component_id)s,
    kit_parent_line_id = %(kit_parent_line_id)s,
    role = %(role)s,
    demand_kind = %(demand_kind)s,
    amount_mode = %(amount_mode)s,
    amount = %(amount)s,
    amount_max = %(amount_max)s,
    unit_id = %(unit_id)s,
    canonical_amount = %(canonical_amount)s,
    conversion_id = %(conversion_id)s,
    scaling_rule_id = %(scaling_rule_id)s,
    optional = %(optional)s,
    note = %(note)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.line_no,
    t.form_id,
    t.product_version_id,
    t.component_id,
    t.kit_parent_line_id,
    t.role,
    t.demand_kind,
    t.amount_mode,
    t.amount,
    t.amount_max,
    t.unit_id,
    t.canonical_amount,
    t.conversion_id,
    t.scaling_rule_id,
    t.optional,
    t.note,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "amount": values["amount"],
        "amount_max": values["amount_max"],
        "amount_mode": values["amount_mode"],
        "canonical_amount": values["canonical_amount"],
        "component_id": values["component_id"],
        "conversion_id": values["conversion_id"],
        "demand_kind": values["demand_kind"],
        "expected_etag": values["expected_etag"],
        "form_id": values["form_id"],
        "kit_parent_line_id": values["kit_parent_line_id"],
        "line_no": values["line_no"],
        "note": values["note"],
        "optional": values["optional"],
        "product_version_id": values["product_version_id"],
        "recipe_version_id": values["recipe_version_id"],
        "role": values["role"],
        "row_id": values["row_id"],
        "scaling_rule_id": values["scaling_rule_id"],
        "unit_id": values["unit_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
