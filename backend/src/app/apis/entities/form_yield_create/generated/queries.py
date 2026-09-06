# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    conditions: str
    input_form_id: UUID
    output_form_id: UUID
    quality: str
    row_id: UUID
    source_id: UUID | None
    yield_ratio: Decimal


SQL = """-- 処理歩留まりを作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.form_yield AS t (
    id,
    input_form_id,
    output_form_id,
    yield_ratio,
    source_id,
    quality,
    conditions
)
VALUES (
    %(row_id)s,
    %(input_form_id)s,
    %(output_form_id)s,
    %(yield_ratio)s,
    %(source_id)s,
    %(quality)s,
    %(conditions)s
)
RETURNING
    t.id,
    t.created_at,
    t.input_form_id,
    t.output_form_id,
    t.yield_ratio,
    t.source_id,
    t.quality,
    t.conditions,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "conditions": values["conditions"],
        "input_form_id": values["input_form_id"],
        "output_form_id": values["output_form_id"],
        "quality": values["quality"],
        "row_id": values["row_id"],
        "source_id": values["source_id"],
        "yield_ratio": values["yield_ratio"],
    }
    return list(connection.execute(SQL, params).fetchall())
