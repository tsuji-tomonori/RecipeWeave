# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    code: str
    completion_cue: str
    definition: str
    name: str
    precondition: str
    row_id: UUID
    status: str


SQL = """-- 標準調理動作を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.operation AS t (
    id,
    code,
    name,
    definition,
    precondition,
    completion_cue,
    status
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(name)s,
    %(definition)s,
    %(precondition)s,
    %(completion_cue)s,
    %(status)s
)
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.definition,
    t.precondition,
    t.completion_cue,
    t.status,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "code": values["code"],
        "completion_cue": values["completion_cue"],
        "definition": values["definition"],
        "name": values["name"],
        "precondition": values["precondition"],
        "row_id": values["row_id"],
        "status": values["status"],
    }
    return list(connection.execute(SQL, params).fetchall())
