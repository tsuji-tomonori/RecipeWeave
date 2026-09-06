# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    expected_etag: str
    menu_id: UUID
    position: int
    recipe_version_id: UUID
    role_option_id: UUID
    row_id: UUID
    servings: Decimal


SQL = """-- 献立の料理を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.menu_item AS t
SET
    menu_id = %(menu_id)s,
    recipe_version_id = %(recipe_version_id)s,
    servings = %(servings)s,
    role_option_id = %(role_option_id)s,
    position = %(position)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND EXISTS (
        SELECT owner_0.id
        FROM recipeweave.menu AS owner_0
        WHERE
            owner_0.id = t.menu_id
            AND owner_0.user_id = %(actor_id)s
    )
RETURNING
    t.id,
    t.created_at,
    t.menu_id,
    t.recipe_version_id,
    t.servings,
    t.role_option_id,
    t.position,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "actor_id": values["actor_id"],
        "expected_etag": values["expected_etag"],
        "menu_id": values["menu_id"],
        "position": values["position"],
        "recipe_version_id": values["recipe_version_id"],
        "role_option_id": values["role_option_id"],
        "row_id": values["row_id"],
        "servings": values["servings"],
    }
    return list(connection.execute(SQL, params).fetchall())
