# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import date, datetime
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    amount: Decimal | None
    edited: bool
    expected_etag: str
    expires_on: date | None
    form_id: UUID
    location: str
    opened_at: datetime | None
    original_amount: Decimal | None
    original_form_id: UUID | None
    original_unit_id: UUID | None
    priority: str
    product_version_id: UUID | None
    quantity_quality: str
    row_id: UUID
    source_import_id: UUID | None
    status: str
    unit_id: UUID
    updated_at: datetime
    user_id: UUID


SQL = """-- 手持ち食材ロットを条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.pantry_lot AS t
SET
    user_id = %(user_id)s,
    form_id = %(form_id)s,
    product_version_id = %(product_version_id)s,
    amount = %(amount)s,
    unit_id = %(unit_id)s,
    expires_on = %(expires_on)s,
    opened_at = %(opened_at)s,
    location = %(location)s,
    priority = %(priority)s,
    status = %(status)s,
    source_import_id = %(source_import_id)s,
    quantity_quality = %(quantity_quality)s,
    original_form_id = %(original_form_id)s,
    original_amount = %(original_amount)s,
    original_unit_id = %(original_unit_id)s,
    updated_at = %(updated_at)s,
    edited = %(edited)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND t.user_id = %(actor_id)s
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.form_id,
    t.product_version_id,
    t.amount,
    t.unit_id,
    t.expires_on,
    t.opened_at,
    t.location,
    t.priority,
    t.status,
    t.source_import_id,
    t.quantity_quality,
    t.original_form_id,
    t.original_amount,
    t.original_unit_id,
    t.updated_at,
    t.edited,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "actor_id": values["actor_id"],
        "amount": values["amount"],
        "edited": values["edited"],
        "expected_etag": values["expected_etag"],
        "expires_on": values["expires_on"],
        "form_id": values["form_id"],
        "location": values["location"],
        "opened_at": values["opened_at"],
        "original_amount": values["original_amount"],
        "original_form_id": values["original_form_id"],
        "original_unit_id": values["original_unit_id"],
        "priority": values["priority"],
        "product_version_id": values["product_version_id"],
        "quantity_quality": values["quantity_quality"],
        "row_id": values["row_id"],
        "source_import_id": values["source_import_id"],
        "status": values["status"],
        "unit_id": values["unit_id"],
        "updated_at": values["updated_at"],
        "user_id": values["user_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
