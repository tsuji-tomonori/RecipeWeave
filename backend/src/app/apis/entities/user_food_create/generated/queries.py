# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    food_id: UUID
    row_id: UUID
    user_id: UUID


SQL = """-- 利用者が追加した独自食材の所有を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.user_food AS t (
    id,
    user_id,
    food_id
)
VALUES (
    %(row_id)s,
    %(user_id)s,
    %(food_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.food_id,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "food_id": values["food_id"],
        "row_id": values["row_id"],
        "user_id": values["user_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
