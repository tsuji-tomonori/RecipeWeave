# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    option_id: UUID
    row_id: UUID
    user_id: UUID
    weight: Decimal


SQL = """-- ユーザーの嗜好を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.user_preference AS t (
    id,
    user_id,
    option_id,
    weight
)
VALUES (
    %(row_id)s,
    %(user_id)s,
    %(option_id)s,
    %(weight)s
)
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.option_id,
    t.weight,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "option_id": values["option_id"],
        "row_id": values["row_id"],
        "user_id": values["user_id"],
        "weight": values["weight"],
    }
    return list(connection.execute(SQL, params).fetchall())
