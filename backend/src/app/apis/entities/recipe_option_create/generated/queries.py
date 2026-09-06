# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    option_id: UUID
    recipe_version_id: UUID
    row_id: UUID


SQL = """-- 版の分類・特徴を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.recipe_option AS t (
    id,
    recipe_version_id,
    option_id
)
VALUES (
    %(row_id)s,
    %(recipe_version_id)s,
    %(option_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.option_id,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "option_id": values["option_id"],
        "recipe_version_id": values["recipe_version_id"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
