# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    expected_etag: str
    row_id: UUID


SQL = """-- 展開済み工程を条件付き削除する。
-- 値は名前付きパラメータで束縛する。
DELETE FROM recipeweave.session_task AS t
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND EXISTS (
        SELECT owner_0.id
        FROM recipeweave.cooking_session AS owner_0
        WHERE
            owner_0.id = t.session_id
            AND EXISTS (
                SELECT owner_1.id
                FROM recipeweave.menu AS owner_1
                WHERE
                    owner_1.id = owner_0.menu_id
                    AND owner_1.user_id = %(actor_id)s
            )
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
        "actor_id": values["actor_id"],
        "expected_etag": values["expected_etag"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
