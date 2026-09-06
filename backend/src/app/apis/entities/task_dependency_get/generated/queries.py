# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    row_id: UUID


SQL = """-- 献立展開後依存を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.before_task_id,
    t.after_task_id,
    t.min_lag_s,
    t.max_lag_s,
    t.reason,
    t.xmin::TEXT AS etag
FROM recipeweave.task_dependency AS t
WHERE
    t.id = %(row_id)s
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
    );
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {"actor_id": values["actor_id"], "row_id": values["row_id"]}
    return list(connection.execute(SQL, params).fetchall())
