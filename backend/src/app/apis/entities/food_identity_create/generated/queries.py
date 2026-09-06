# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    code: str
    name: str
    normalizer_version: str
    row_id: UUID


SQL = """-- 料理同一性上の食品を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.food_identity AS t (
    id,
    code,
    name,
    normalizer_version
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(name)s,
    %(normalizer_version)s
)
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.normalizer_version,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "code": values["code"],
        "name": values["name"],
        "normalizer_version": values["normalizer_version"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
