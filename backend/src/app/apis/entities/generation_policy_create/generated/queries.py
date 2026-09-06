# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection
from psycopg.types.json import Jsonb


class Parameters(TypedDict):
    model_identifier: str
    parameter_json: Jsonb
    prompt_template: str
    release_id: UUID
    row_id: UUID
    schema_version: str
    version: str


SQL = """-- AI生成方針版を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.generation_policy AS t (
    id,
    version,
    prompt_template,
    model_identifier,
    parameter_json,
    schema_version,
    release_id
)
VALUES (
    %(row_id)s,
    %(version)s,
    %(prompt_template)s,
    %(model_identifier)s,
    %(parameter_json)s,
    %(schema_version)s,
    %(release_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.version,
    t.prompt_template,
    t.model_identifier,
    t.parameter_json,
    t.schema_version,
    t.release_id,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "model_identifier": values["model_identifier"],
        "parameter_json": values["parameter_json"],
        "prompt_template": values["prompt_template"],
        "release_id": values["release_id"],
        "row_id": values["row_id"],
        "schema_version": values["schema_version"],
        "version": values["version"],
    }
    return list(connection.execute(SQL, params).fetchall())
