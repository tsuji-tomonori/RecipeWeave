# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    amount: Decimal | None
    decision: str
    expected_etag: str
    form_id: UUID | None
    import_id: UUID
    line_no: int
    pantry_lot_id: UUID | None
    product_version_id: UUID | None
    raw_name: str
    row_id: UUID
    unit_id: UUID | None


SQL = """-- レシートの商品候補と確定した在庫の対応を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.receipt_line AS t
SET
    import_id = %(import_id)s,
    line_no = %(line_no)s,
    raw_name = %(raw_name)s,
    form_id = %(form_id)s,
    product_version_id = %(product_version_id)s,
    amount = %(amount)s,
    unit_id = %(unit_id)s,
    decision = %(decision)s,
    pantry_lot_id = %(pantry_lot_id)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND EXISTS (
        SELECT owner_0.id
        FROM recipeweave.receipt_import AS owner_0
        WHERE
            owner_0.id = t.import_id
            AND owner_0.user_id = %(actor_id)s
    )
RETURNING
    t.id,
    t.created_at,
    t.import_id,
    t.line_no,
    t.raw_name,
    t.form_id,
    t.product_version_id,
    t.amount,
    t.unit_id,
    t.decision,
    t.pantry_lot_id,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "actor_id": values["actor_id"],
        "amount": values["amount"],
        "decision": values["decision"],
        "expected_etag": values["expected_etag"],
        "form_id": values["form_id"],
        "import_id": values["import_id"],
        "line_no": values["line_no"],
        "pantry_lot_id": values["pantry_lot_id"],
        "product_version_id": values["product_version_id"],
        "raw_name": values["raw_name"],
        "row_id": values["row_id"],
        "unit_id": values["unit_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
