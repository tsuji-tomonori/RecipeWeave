# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    axis_id: UUID
    code: str
    definition: str
    label: str
    parent_id: UUID | None
    row_id: UUID
    status: str


SQL = """-- 軸候補値を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.axis_option AS t (
    id,
    axis_id,
    code,
    label,
    definition,
    parent_id,
    status
)
VALUES (
    %(row_id)s,
    %(axis_id)s,
    %(code)s,
    %(label)s,
    %(definition)s,
    %(parent_id)s,
    %(status)s
)
RETURNING
    t.id,
    t.created_at,
    t.axis_id,
    t.code,
    t.label,
    t.definition,
    t.parent_id,
    t.status,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "axis_id": values["axis_id"],
        "code": values["code"],
        "definition": values["definition"],
        "label": values["label"],
        "parent_id": values["parent_id"],
        "row_id": values["row_id"],
        "status": values["status"],
    }
    return list(connection.execute(SQL, params).fetchall())
