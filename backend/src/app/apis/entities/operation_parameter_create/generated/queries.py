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
    max_value: Decimal | None
    min_value: Decimal | None
    name: str
    operation_id: UUID
    required: bool
    row_id: UUID
    unit_id: UUID | None
    value_type: str


SQL = """-- 動作パラメータ定義を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.operation_parameter AS t (
    id,
    operation_id,
    code,
    name,
    value_type,
    unit_id,
    required,
    min_value,
    max_value,
    allowed_values
)
VALUES (
    %(row_id)s,
    %(operation_id)s,
    %(code)s,
    %(name)s,
    %(value_type)s,
    %(unit_id)s,
    %(required)s,
    %(min_value)s,
    %(max_value)s,
    %(allowed_values)s
)
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
