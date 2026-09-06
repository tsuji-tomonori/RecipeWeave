# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    expected_etag: str
    form_id: UUID
    job_id: UUID
    role: str
    row_id: UUID


SQL = """-- 生成の食材入力を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.generation_food AS t
SET
    job_id = %(job_id)s,
    form_id = %(form_id)s,
    role = %(role)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.job_id,
    t.form_id,
    t.role,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "expected_etag": values["expected_etag"],
        "form_id": values["form_id"],
        "job_id": values["job_id"],
        "role": values["role"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
