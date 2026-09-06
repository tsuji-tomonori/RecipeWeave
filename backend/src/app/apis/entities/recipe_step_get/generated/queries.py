# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    row_id: UUID


SQL = """-- 調理工程節点を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
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
    t.xmin::TEXT AS etag
FROM recipeweave.recipe_step AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {"row_id": values["row_id"]}
    return list(connection.execute(SQL, params).fetchall())
