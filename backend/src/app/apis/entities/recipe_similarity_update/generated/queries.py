# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    algorithm_version: str
    expected_etag: str
    explanation: str
    left_version_id: UUID
    right_version_id: UUID
    row_id: UUID
    score: Decimal


SQL = """-- 近似レシピ関係を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.recipe_similarity AS t
SET
    left_version_id = %(left_version_id)s,
    right_version_id = %(right_version_id)s,
    algorithm_version = %(algorithm_version)s,
    score = %(score)s,
    explanation = %(explanation)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.left_version_id,
    t.right_version_id,
    t.algorithm_version,
    t.score,
    t.explanation,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "algorithm_version": values["algorithm_version"],
        "expected_etag": values["expected_etag"],
        "explanation": values["explanation"],
        "left_version_id": values["left_version_id"],
        "right_version_id": values["right_version_id"],
        "row_id": values["row_id"],
        "score": values["score"],
    }
    return list(connection.execute(SQL, params).fetchall())
