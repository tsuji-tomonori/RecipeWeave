# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    bool_value: bool | None
    expected_etag: str
    number_value: Decimal | None
    parameter_id: UUID
    row_id: UUID
    step_id: UUID
    text_value: str | None


SQL = """-- 工程の型付きパラメータを条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.step_parameter AS t
SET
    step_id = %(step_id)s,
    parameter_id = %(parameter_id)s,
    number_value = %(number_value)s,
    text_value = %(text_value)s,
    bool_value = %(bool_value)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.step_id,
    t.parameter_id,
    t.number_value,
    t.text_value,
    t.bool_value,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "bool_value": values["bool_value"],
        "expected_etag": values["expected_etag"],
        "number_value": values["number_value"],
        "parameter_id": values["parameter_id"],
        "row_id": values["row_id"],
        "step_id": values["step_id"],
        "text_value": values["text_value"],
    }
    return list(connection.execute(SQL, params).fetchall())
