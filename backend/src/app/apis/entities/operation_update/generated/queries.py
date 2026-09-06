# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    code: str
    completion_cue: str
    definition: str
    expected_etag: str
    name: str
    precondition: str
    row_id: UUID
    status: str


SQL = """-- 標準調理動作を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.operation AS t
SET
    code = %(code)s,
    name = %(name)s,
    definition = %(definition)s,
    precondition = %(precondition)s,
    completion_cue = %(completion_cue)s,
    status = %(status)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
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
        "expected_etag": values["expected_etag"],
        "name": values["name"],
        "precondition": values["precondition"],
        "row_id": values["row_id"],
        "status": values["status"],
    }
    return list(connection.execute(SQL, params).fetchall())
