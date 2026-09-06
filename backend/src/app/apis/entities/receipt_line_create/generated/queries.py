# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    amount: Decimal | None
    decision: str
    form_id: UUID | None
    import_id: UUID
    line_no: int
    pantry_lot_id: UUID | None
    product_version_id: UUID | None
    raw_name: str
    row_id: UUID
    unit_id: UUID | None


SQL = """-- レシートの商品候補と確定した在庫の対応を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.receipt_line AS t (
    id,
    import_id,
    line_no,
    raw_name,
    form_id,
    product_version_id,
    amount,
    unit_id,
    decision,
    pantry_lot_id
)
VALUES (
    %(row_id)s,
    %(import_id)s,
    %(line_no)s,
    %(raw_name)s,
    %(form_id)s,
    %(product_version_id)s,
    %(amount)s,
    %(unit_id)s,
    %(decision)s,
    %(pantry_lot_id)s
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
        "amount": values["amount"],
        "decision": values["decision"],
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
