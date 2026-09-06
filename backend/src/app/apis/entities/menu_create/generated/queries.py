# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    name: str
    row_id: UUID
    servings: Decimal
    user_id: UUID


SQL = """-- 献立を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.menu AS t (
    id,
    user_id,
    name,
    servings,
    revision
)
VALUES (
    %(row_id)s,
    %(user_id)s,
    %(name)s,
    %(servings)s,
    1
)
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.name,
    t.servings,
    t.revision,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "name": values["name"],
        "row_id": values["row_id"],
        "servings": values["servings"],
        "user_id": values["user_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
