# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    after_task_id: UUID
    before_task_id: UUID
    max_lag_s: int | None
    min_lag_s: int
    reason: str
    row_id: UUID


SQL = """-- 献立展開後依存を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.task_dependency AS t (
    id,
    before_task_id,
    after_task_id,
    min_lag_s,
    max_lag_s,
    reason
)
VALUES (
    %(row_id)s,
    %(before_task_id)s,
    %(after_task_id)s,
    %(min_lag_s)s,
    %(max_lag_s)s,
    %(reason)s
)
RETURNING
    t.id,
    t.created_at,
    t.before_task_id,
    t.after_task_id,
    t.min_lag_s,
    t.max_lag_s,
    t.reason,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "after_task_id": values["after_task_id"],
        "before_task_id": values["before_task_id"],
        "max_lag_s": values["max_lag_s"],
        "min_lag_s": values["min_lag_s"],
        "reason": values["reason"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
