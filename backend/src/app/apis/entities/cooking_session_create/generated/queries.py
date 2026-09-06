# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import datetime
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection
from psycopg.types.json import Jsonb


class Parameters(TypedDict):
    current_task_index: int
    input_hash: str
    input_snapshot: Jsonb
    menu_id: UUID
    menu_revision: int
    planner_version: str
    row_id: UUID
    status: str
    target_at: datetime | None


SQL = """-- 調理計画実行を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.cooking_session AS t (
    id,
    menu_id,
    menu_revision,
    status,
    target_at,
    planner_version,
    input_snapshot,
    input_hash,
    current_task_index
)
VALUES (
    %(row_id)s,
    %(menu_id)s,
    %(menu_revision)s,
    %(status)s,
    %(target_at)s,
    %(planner_version)s,
    %(input_snapshot)s,
    %(input_hash)s,
    %(current_task_index)s
)
RETURNING
    t.id,
    t.created_at,
    t.menu_id,
    t.menu_revision,
    t.status,
    t.target_at,
    t.planner_version,
    t.input_snapshot,
    t.input_hash,
    t.current_task_index,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "current_task_index": values["current_task_index"],
        "input_hash": values["input_hash"],
        "input_snapshot": values["input_snapshot"],
        "menu_id": values["menu_id"],
        "menu_revision": values["menu_revision"],
        "planner_version": values["planner_version"],
        "row_id": values["row_id"],
        "status": values["status"],
        "target_at": values["target_at"],
    }
    return list(connection.execute(SQL, params).fetchall())
