# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    attention: str
    completion_cue: str
    duration_max_s: int
    duration_min_s: int
    instruction: str
    operation_id: UUID
    recipe_version_id: UUID
    row_id: UUID
    scaling_rule_id: UUID
    step_no: int
    title: str | None


SQL = """-- 調理工程節点を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.recipe_step AS t (
    id,
    recipe_version_id,
    step_no,
    operation_id,
    instruction,
    attention,
    duration_min_s,
    duration_max_s,
    scaling_rule_id,
    completion_cue,
    title
)
VALUES (
    %(row_id)s,
    %(recipe_version_id)s,
    %(step_no)s,
    %(operation_id)s,
    %(instruction)s,
    %(attention)s,
    %(duration_min_s)s,
    %(duration_max_s)s,
    %(scaling_rule_id)s,
    %(completion_cue)s,
    %(title)s
)
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.step_no,
    t.operation_id,
    t.instruction,
    t.attention,
    t.duration_min_s,
    t.duration_max_s,
    t.scaling_rule_id,
    t.completion_cue,
    t.title,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "attention": values["attention"],
        "completion_cue": values["completion_cue"],
        "duration_max_s": values["duration_max_s"],
        "duration_min_s": values["duration_min_s"],
        "instruction": values["instruction"],
        "operation_id": values["operation_id"],
        "recipe_version_id": values["recipe_version_id"],
        "row_id": values["row_id"],
        "scaling_rule_id": values["scaling_rule_id"],
        "step_no": values["step_no"],
        "title": values["title"],
    }
    return list(connection.execute(SQL, params).fetchall())
