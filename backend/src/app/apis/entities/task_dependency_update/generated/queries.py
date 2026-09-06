# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    after_task_id: UUID
    before_task_id: UUID
    expected_etag: str
    max_lag_s: int | None
    min_lag_s: int
    reason: str
    row_id: UUID


SQL = """-- 献立展開後依存を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.task_dependency AS t
SET
    before_task_id = %(before_task_id)s,
    after_task_id = %(after_task_id)s,
    min_lag_s = %(min_lag_s)s,
    max_lag_s = %(max_lag_s)s,
    reason = %(reason)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND EXISTS (
        SELECT owner_0.id
        FROM recipeweave.session_task AS owner_0
        WHERE
            owner_0.id = t.before_task_id
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
        "actor_id": values["actor_id"],
        "after_task_id": values["after_task_id"],
        "before_task_id": values["before_task_id"],
        "expected_etag": values["expected_etag"],
        "max_lag_s": values["max_lag_s"],
        "min_lag_s": values["min_lag_s"],
        "reason": values["reason"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
