# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    row_id: UUID


SQL = """-- 献立の料理を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.menu_id,
    t.recipe_version_id,
    t.servings,
    t.role_option_id,
    t.position,
    t.xmin::TEXT AS etag
FROM recipeweave.menu_item AS t
WHERE
    t.id = %(row_id)s
    AND EXISTS (
        SELECT owner_0.id
        FROM recipeweave.menu AS owner_0
        WHERE
            owner_0.id = t.menu_id
            AND owner_0.user_id = %(actor_id)s
    );
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {"actor_id": values["actor_id"], "row_id": values["row_id"]}
    return list(connection.execute(SQL, params).fetchall())
