# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    expected_etag: str
    row_id: UUID


SQL = """-- 手持ち食材ロットを条件付き削除する。
-- 値は名前付きパラメータで束縛する。
DELETE FROM recipeweave.pantry_lot AS t
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
        "expected_etag": values["expected_etag"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
