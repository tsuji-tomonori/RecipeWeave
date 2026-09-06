# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    amount: Decimal | None
    form_id: UUID
    name: str
    product_version_id: UUID
    quality: str
    row_id: UUID
    unit_id: UUID | None


SQL = """-- セット内構成品を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.product_component AS t (
    id,
    product_version_id,
    form_id,
    name,
    amount,
    unit_id,
    quality
)
VALUES (
    %(row_id)s,
    %(product_version_id)s,
    %(form_id)s,
    %(name)s,
    %(amount)s,
    %(unit_id)s,
    %(quality)s
)
RETURNING
    t.id,
    t.created_at,
    t.product_version_id,
    t.form_id,
    t.name,
    t.amount,
    t.unit_id,
    t.quality,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "amount": values["amount"],
        "form_id": values["form_id"],
        "name": values["name"],
        "product_version_id": values["product_version_id"],
        "quality": values["quality"],
        "row_id": values["row_id"],
        "unit_id": values["unit_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
