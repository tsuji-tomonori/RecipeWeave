# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection
from psycopg.types.json import Jsonb


class Parameters(TypedDict):
    input_snapshot: Jsonb
    job_id: UUID | None
    policy_id: UUID
    raw_output_hash: str
    raw_output_uri: str | None
    recipe_version_id: UUID
    row_id: UUID


SQL = """-- 生成結果の出自を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.generation_result AS t (
    id,
    recipe_version_id,
    job_id,
    policy_id,
    input_snapshot,
    raw_output_uri,
    raw_output_hash
)
VALUES (
    %(row_id)s,
    %(recipe_version_id)s,
    %(job_id)s,
    %(policy_id)s,
    %(input_snapshot)s,
    %(raw_output_uri)s,
    %(raw_output_hash)s
)
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.job_id,
    t.policy_id,
    t.input_snapshot,
    t.raw_output_uri,
    t.raw_output_hash,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "input_snapshot": values["input_snapshot"],
        "job_id": values["job_id"],
        "policy_id": values["policy_id"],
        "raw_output_hash": values["raw_output_hash"],
        "raw_output_uri": values["raw_output_uri"],
        "recipe_version_id": values["recipe_version_id"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
