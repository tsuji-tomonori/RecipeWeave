# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    amount: Decimal
    basis_amount: Decimal
    basis_unit_id: UUID
    form_id: UUID | None
    nutrient_id: UUID
    product_version_id: UUID | None
    row_id: UUID
    source_id: UUID


SQL = """-- 形態・商品別栄養値を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.nutrition_fact AS t (
    id,
    form_id,
    product_version_id,
    nutrient_id,
    amount,
    basis_amount,
    basis_unit_id,
    source_id
)
VALUES (
    %(row_id)s,
    %(form_id)s,
    %(product_version_id)s,
    %(nutrient_id)s,
    %(amount)s,
    %(basis_amount)s,
    %(basis_unit_id)s,
    %(source_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.form_id,
    t.product_version_id,
    t.nutrient_id,
    t.amount,
    t.basis_amount,
    t.basis_unit_id,
    t.source_id,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "amount": values["amount"],
        "basis_amount": values["basis_amount"],
        "basis_unit_id": values["basis_unit_id"],
        "form_id": values["form_id"],
        "nutrient_id": values["nutrient_id"],
        "product_version_id": values["product_version_id"],
        "row_id": values["row_id"],
        "source_id": values["source_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
