# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import datetime
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection
from psycopg.types.json import Jsonb


class Parameters(TypedDict):
    evaluated_at: datetime
    evidence: Jsonb
    recipe_version_id: UUID
    row_id: UUID
    rule_id: UUID
    state: str
    validator_version: str


SQL = """-- 公開前評価結果を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.validation_result AS t (
    id,
    recipe_version_id,
    rule_id,
    state,
    evidence,
    validator_version,
    evaluated_at
)
VALUES (
    %(row_id)s,
    %(recipe_version_id)s,
    %(rule_id)s,
    %(state)s,
    %(evidence)s,
    %(validator_version)s,
    %(evaluated_at)s
)
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.rule_id,
    t.state,
    t.evidence,
    t.validator_version,
    t.evaluated_at,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "evaluated_at": values["evaluated_at"],
        "evidence": values["evidence"],
        "recipe_version_id": values["recipe_version_id"],
        "row_id": values["row_id"],
        "rule_id": values["rule_id"],
        "state": values["state"],
        "validator_version": values["validator_version"],
    }
    return list(connection.execute(SQL, params).fetchall())
