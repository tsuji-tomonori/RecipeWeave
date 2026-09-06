# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    job_id: UUID
    option_id: UUID
    row_id: UUID


SQL = """-- 生成軸の選択値を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.generation_choice AS t (
    id,
    job_id,
    option_id
)
VALUES (
    %(row_id)s,
    %(job_id)s,
    %(option_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.job_id,
    t.option_id,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "job_id": values["job_id"],
        "option_id": values["option_id"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
