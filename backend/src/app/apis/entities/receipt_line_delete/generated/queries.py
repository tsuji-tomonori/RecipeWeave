# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    expected_etag: str
    row_id: UUID


SQL = """-- レシートの商品候補と確定した在庫の対応を条件付き削除する。
-- 値は名前付きパラメータで束縛する。
DELETE FROM recipeweave.receipt_line AS t
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
        "expected_etag": values["expected_etag"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
