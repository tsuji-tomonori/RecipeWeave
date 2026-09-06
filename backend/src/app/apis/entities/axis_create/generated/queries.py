# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    code: str
    name: str
    purpose: str
    release_id: UUID
    row_id: UUID
    selection: str
    status: str


SQL = """-- 組み合わせ軸を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.axis AS t (
    id,
    code,
    name,
    purpose,
    selection,
    release_id,
    status
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(name)s,
    %(purpose)s,
    %(selection)s,
    %(release_id)s,
    %(status)s
)
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.purpose,
    t.selection,
    t.release_id,
    t.status,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "code": values["code"],
        "name": values["name"],
        "purpose": values["purpose"],
        "release_id": values["release_id"],
        "row_id": values["row_id"],
        "selection": values["selection"],
        "status": values["status"],
    }
    return list(connection.execute(SQL, params).fetchall())
