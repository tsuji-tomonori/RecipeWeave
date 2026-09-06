# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    after_step_id: UUID
    before_step_id: UUID
    kind: str
    max_lag_s: int | None
    min_lag_s: int
    row_id: UUID


SQL = """-- 工程依存辺を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.step_dependency AS t (
    id,
    before_step_id,
    after_step_id,
    kind,
    min_lag_s,
    max_lag_s
)
VALUES (
    %(row_id)s,
    %(before_step_id)s,
    %(after_step_id)s,
    %(kind)s,
    %(min_lag_s)s,
    %(max_lag_s)s
)
RETURNING
    t.id,
    t.created_at,
    t.before_step_id,
    t.after_step_id,
    t.kind,
    t.min_lag_s,
    t.max_lag_s,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "after_step_id": values["after_step_id"],
        "before_step_id": values["before_step_id"],
        "kind": values["kind"],
        "max_lag_s": values["max_lag_s"],
        "min_lag_s": values["min_lag_s"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
