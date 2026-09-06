# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import date
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    drain_amount: Decimal | None
    form_id: UUID
    net_amount: Decimal
    preparation_note: str
    product_id: UUID
    row_id: UUID
    source_id: UUID
    unit_id: UUID
    valid_from: date
    version: int


SQL = """-- 商品仕様版を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.product_version AS t (
    id,
    product_id,
    version,
    form_id,
    net_amount,
    unit_id,
    drain_amount,
    source_id,
    preparation_note,
    valid_from
)
VALUES (
    %(row_id)s,
    %(product_id)s,
    %(version)s,
    %(form_id)s,
    %(net_amount)s,
    %(unit_id)s,
    %(drain_amount)s,
    %(source_id)s,
    %(preparation_note)s,
    %(valid_from)s
)
RETURNING
    t.id,
    t.created_at,
    t.product_id,
    t.version,
    t.form_id,
    t.net_amount,
    t.unit_id,
    t.drain_amount,
    t.source_id,
    t.preparation_note,
    t.valid_from,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "drain_amount": values["drain_amount"],
        "form_id": values["form_id"],
        "net_amount": values["net_amount"],
        "preparation_note": values["preparation_note"],
        "product_id": values["product_id"],
        "row_id": values["row_id"],
        "source_id": values["source_id"],
        "unit_id": values["unit_id"],
        "valid_from": values["valid_from"],
        "version": values["version"],
    }
    return list(connection.execute(SQL, params).fetchall())
