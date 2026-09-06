# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    attempts: int
    design_key: str
    job_id: UUID | None
    ordinal: int
    reason_code: str | None
    recipe_version_id: UUID | None
    row_id: UUID
    state: str
    template_id: UUID


SQL = """-- 試行済み設計点の台帳を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.candidate_attempt AS t (
    id,
    template_id,
    ordinal,
    design_key,
    job_id,
    state,
    reason_code,
    recipe_version_id,
    attempts
)
VALUES (
    %(row_id)s,
    %(template_id)s,
    %(ordinal)s,
    %(design_key)s,
    %(job_id)s,
    %(state)s,
    %(reason_code)s,
    %(recipe_version_id)s,
    %(attempts)s
)
RETURNING
    t.id,
    t.created_at,
    t.template_id,
    t.ordinal,
    t.design_key,
    t.job_id,
    t.state,
    t.reason_code,
    t.recipe_version_id,
    t.attempts,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "attempts": values["attempts"],
        "design_key": values["design_key"],
        "job_id": values["job_id"],
        "ordinal": values["ordinal"],
        "reason_code": values["reason_code"],
        "recipe_version_id": values["recipe_version_id"],
        "row_id": values["row_id"],
        "state": values["state"],
        "template_id": values["template_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
