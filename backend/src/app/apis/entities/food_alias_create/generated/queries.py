# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    alias: str
    food_id: UUID
    locale: str
    row_id: UUID


SQL = """-- 食材別名を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.food_alias AS t (
    id,
    food_id,
    alias,
    locale
)
VALUES (
    %(row_id)s,
    %(food_id)s,
    %(alias)s,
    %(locale)s
)
RETURNING
    t.id,
    t.created_at,
    t.food_id,
    t.alias,
    t.locale,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "alias": values["alias"],
        "food_id": values["food_id"],
        "locale": values["locale"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
