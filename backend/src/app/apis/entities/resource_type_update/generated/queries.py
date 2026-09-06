# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    capacity_unit_id: UUID | None
    code: str
    expected_etag: str
    name: str
    row_id: UUID
    status: str


SQL = """-- 道具・設備・作業者種別を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.resource_type AS t
SET
    code = %(code)s,
    name = %(name)s,
    capacity_unit_id = %(capacity_unit_id)s,
    status = %(status)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.capacity_unit_id,
    t.status,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "capacity_unit_id": values["capacity_unit_id"],
        "code": values["code"],
        "expected_etag": values["expected_etag"],
        "name": values["name"],
        "row_id": values["row_id"],
        "status": values["status"],
    }
    return list(connection.execute(SQL, params).fetchall())
