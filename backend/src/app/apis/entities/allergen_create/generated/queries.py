# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    code: str
    name: str
    row_id: UUID
    source_id: UUID | None


SQL = """-- アレルゲン概念を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.allergen AS t (
    id,
    code,
    name,
    source_id
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(name)s,
    %(source_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.source_id,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "code": values["code"],
        "name": values["name"],
        "row_id": values["row_id"],
        "source_id": values["source_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
