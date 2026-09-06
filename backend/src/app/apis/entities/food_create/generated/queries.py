# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    code: str
    kind: str
    name: str
    parent_id: UUID | None
    release_id: UUID
    row_id: UUID
    status: str


SQL = """-- 購入・利用食材概念を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.food AS t (
    id,
    code,
    name,
    kind,
    parent_id,
    release_id,
    status
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(name)s,
    %(kind)s,
    %(parent_id)s,
    %(release_id)s,
    %(status)s
)
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.kind,
    t.parent_id,
    t.release_id,
    t.status,
    t.owner_id,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "code": values["code"],
        "kind": values["kind"],
        "name": values["name"],
        "parent_id": values["parent_id"],
        "release_id": values["release_id"],
        "row_id": values["row_id"],
        "status": values["status"],
    }
    return list(connection.execute(SQL, params).fetchall())
