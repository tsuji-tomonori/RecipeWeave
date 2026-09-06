# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import datetime
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    kind: str
    occurred_at: datetime
    recipe_version_id: UUID
    request_key: str
    row_id: UUID
    user_id: UUID


SQL = """-- 提案・調理履歴を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.user_recipe_event AS t (
    id,
    user_id,
    recipe_version_id,
    kind,
    occurred_at,
    request_key
)
VALUES (
    %(row_id)s,
    %(user_id)s,
    %(recipe_version_id)s,
    %(kind)s,
    %(occurred_at)s,
    %(request_key)s
)
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.recipe_version_id,
    t.kind,
    t.occurred_at,
    t.request_key,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "kind": values["kind"],
        "occurred_at": values["occurred_at"],
        "recipe_version_id": values["recipe_version_id"],
        "request_key": values["request_key"],
        "row_id": values["row_id"],
        "user_id": values["user_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
