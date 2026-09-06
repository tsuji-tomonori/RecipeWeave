# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    expected_etag: str
    name: str
    row_id: UUID
    servings: Decimal
    user_id: UUID


SQL = """-- 献立を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.menu AS t
SET
    user_id = %(user_id)s,
    name = %(name)s,
    servings = %(servings)s,
    revision = t.revision + 1
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND t.user_id = %(actor_id)s
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
        "actor_id": values["actor_id"],
        "expected_etag": values["expected_etag"],
        "name": values["name"],
        "row_id": values["row_id"],
        "servings": values["servings"],
        "user_id": values["user_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
