# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    code: str
    dimension: str
    expected_etag: str
    factor: Decimal
    name: str
    offset: Decimal
    row_id: UUID
    status: str


SQL = """-- 単位を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.unit AS t
SET
    code = %(code)s,
    name = %(name)s,
    dimension = %(dimension)s,
    factor = %(factor)s,
    "offset" = %(offset)s,
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
    t.dimension,
    t.factor,
    t."offset",
    t.status,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "code": values["code"],
        "dimension": values["dimension"],
        "expected_etag": values["expected_etag"],
        "factor": values["factor"],
        "name": values["name"],
        "offset": values["offset"],
        "row_id": values["row_id"],
        "status": values["status"],
    }
    return list(connection.execute(SQL, params).fetchall())
