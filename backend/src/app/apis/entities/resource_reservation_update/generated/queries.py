# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    end_s: int
    expected_etag: str
    quantity: int
    resource_id: UUID
    row_id: UUID
    start_s: int
    task_id: UUID


SQL = """-- 資源の予約を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.resource_reservation AS t
SET
    task_id = %(task_id)s,
    resource_id = %(resource_id)s,
    start_s = %(start_s)s,
    end_s = %(end_s)s,
    quantity = %(quantity)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND EXISTS (
        SELECT owner_0.id
        FROM recipeweave.session_task AS owner_0
        WHERE
            owner_0.id = t.task_id
            AND EXISTS (
                SELECT owner_1.id
                FROM recipeweave.cooking_session AS owner_1
                WHERE
                    owner_1.id = owner_0.session_id
                    AND EXISTS (
                        SELECT owner_2.id
                        FROM recipeweave.menu AS owner_2
                        WHERE
                            owner_2.id = owner_1.menu_id
                            AND owner_2.user_id = %(actor_id)s
                    )
            )
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
        "actor_id": values["actor_id"],
        "end_s": values["end_s"],
        "expected_etag": values["expected_etag"],
        "quantity": values["quantity"],
        "resource_id": values["resource_id"],
        "row_id": values["row_id"],
        "start_s": values["start_s"],
        "task_id": values["task_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
