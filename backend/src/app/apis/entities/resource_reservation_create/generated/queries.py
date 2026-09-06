# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    end_s: int
    quantity: int
    resource_id: UUID
    row_id: UUID
    start_s: int
    task_id: UUID


SQL = """-- 資源の予約を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.resource_reservation AS t (
    id,
    task_id,
    resource_id,
    start_s,
    end_s,
    quantity
)
VALUES (
    %(row_id)s,
    %(task_id)s,
    %(resource_id)s,
    %(start_s)s,
    %(end_s)s,
    %(quantity)s
)
RETURNING
    t.id,
    t.created_at,
    t.task_id,
    t.resource_id,
    t.start_s,
    t.end_s,
    t.quantity,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "end_s": values["end_s"],
        "quantity": values["quantity"],
        "resource_id": values["resource_id"],
        "row_id": values["row_id"],
        "start_s": values["start_s"],
        "task_id": values["task_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
