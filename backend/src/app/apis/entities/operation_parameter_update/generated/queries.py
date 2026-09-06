# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection
from psycopg.types.json import Jsonb


class Parameters(TypedDict):
    allowed_values: Jsonb | None
    code: str
    expected_etag: str
    max_value: Decimal | None
    min_value: Decimal | None
    name: str
    operation_id: UUID
    required: bool
    row_id: UUID
    unit_id: UUID | None
    value_type: str


SQL = """-- 動作パラメータ定義を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.operation_parameter AS t
SET
    operation_id = %(operation_id)s,
    code = %(code)s,
    name = %(name)s,
    value_type = %(value_type)s,
    unit_id = %(unit_id)s,
    required = %(required)s,
    min_value = %(min_value)s,
    max_value = %(max_value)s,
    allowed_values = %(allowed_values)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.operation_id,
    t.code,
    t.name,
    t.value_type,
    t.unit_id,
    t.required,
    t.min_value,
    t.max_value,
    t.allowed_values,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "allowed_values": values["allowed_values"],
        "code": values["code"],
        "expected_etag": values["expected_etag"],
        "max_value": values["max_value"],
        "min_value": values["min_value"],
        "name": values["name"],
        "operation_id": values["operation_id"],
        "required": values["required"],
        "row_id": values["row_id"],
        "unit_id": values["unit_id"],
        "value_type": values["value_type"],
    }
    return list(connection.execute(SQL, params).fetchall())
