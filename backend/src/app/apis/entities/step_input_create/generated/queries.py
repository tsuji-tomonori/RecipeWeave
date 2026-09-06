# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    fraction: Decimal
    material_id: UUID
    row_id: UUID
    step_id: UUID


SQL = """-- 工程への材料受渡しを作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.step_input AS t (
    id,
    step_id,
    material_id,
    fraction
)
VALUES (
    %(row_id)s,
    %(step_id)s,
    %(material_id)s,
    %(fraction)s
)
RETURNING
    t.id,
    t.created_at,
    t.step_id,
    t.material_id,
    t.fraction,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "fraction": values["fraction"],
        "material_id": values["material_id"],
        "row_id": values["row_id"],
        "step_id": values["step_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
