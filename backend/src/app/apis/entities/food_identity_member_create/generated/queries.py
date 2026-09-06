# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    food_id: UUID
    identity_id: UUID
    normalizer_version: str
    reason: str
    row_id: UUID


SQL = """-- 購買食品から同一性への対応を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.food_identity_member AS t (
    id,
    food_id,
    identity_id,
    normalizer_version,
    reason
)
VALUES (
    %(row_id)s,
    %(food_id)s,
    %(identity_id)s,
    %(normalizer_version)s,
    %(reason)s
)
RETURNING
    t.id,
    t.created_at,
    t.food_id,
    t.identity_id,
    t.normalizer_version,
    t.reason,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "food_id": values["food_id"],
        "identity_id": values["identity_id"],
        "normalizer_version": values["normalizer_version"],
        "reason": values["reason"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
