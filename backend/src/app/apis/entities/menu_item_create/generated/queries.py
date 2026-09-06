# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    menu_id: UUID
    position: int
    recipe_version_id: UUID
    role_option_id: UUID
    row_id: UUID
    servings: Decimal


SQL = """-- 献立の料理を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.menu_item AS t (
    id,
    menu_id,
    recipe_version_id,
    servings,
    role_option_id,
    position
)
VALUES (
    %(row_id)s,
    %(menu_id)s,
    %(recipe_version_id)s,
    %(servings)s,
    %(role_option_id)s,
    %(position)s
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
        "menu_id": values["menu_id"],
        "position": values["position"],
        "recipe_version_id": values["recipe_version_id"],
        "role_option_id": values["role_option_id"],
        "row_id": values["row_id"],
        "servings": values["servings"],
    }
    return list(connection.execute(SQL, params).fetchall())
