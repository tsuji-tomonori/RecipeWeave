# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import datetime
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actual_end_at: datetime | None
    actual_start_at: datetime | None
    batch_no: int
    menu_item_id: UUID
    planned_end_s: int
    planned_start_s: int
    row_id: UUID
    session_id: UUID
    status: str
    step_id: UUID
    timer_duration_s: int | None
    timer_started_at: datetime | None


SQL = """-- 展開済み工程を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.session_task AS t (
    id,
    session_id,
    menu_item_id,
    step_id,
    batch_no,
    planned_start_s,
    planned_end_s,
    status,
    actual_start_at,
    actual_end_at,
    timer_started_at,
    timer_duration_s
)
VALUES (
    %(row_id)s,
    %(session_id)s,
    %(menu_item_id)s,
    %(step_id)s,
    %(batch_no)s,
    %(planned_start_s)s,
    %(planned_end_s)s,
    %(status)s,
    %(actual_start_at)s,
    %(actual_end_at)s,
    %(timer_started_at)s,
    %(timer_duration_s)s
)
RETURNING
    t.id,
    t.created_at,
    t.session_id,
    t.menu_item_id,
    t.step_id,
    t.batch_no,
    t.planned_start_s,
    t.planned_end_s,
    t.status,
    t.actual_start_at,
    t.actual_end_at,
    t.timer_started_at,
    t.timer_duration_s,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "actual_end_at": values["actual_end_at"],
        "actual_start_at": values["actual_start_at"],
        "batch_no": values["batch_no"],
        "menu_item_id": values["menu_item_id"],
        "planned_end_s": values["planned_end_s"],
        "planned_start_s": values["planned_start_s"],
        "row_id": values["row_id"],
        "session_id": values["session_id"],
        "status": values["status"],
        "step_id": values["step_id"],
        "timer_duration_s": values["timer_duration_s"],
        "timer_started_at": values["timer_started_at"],
    }
    return list(connection.execute(SQL, params).fetchall())
