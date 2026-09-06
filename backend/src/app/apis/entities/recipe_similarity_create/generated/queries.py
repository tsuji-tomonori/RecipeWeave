# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    algorithm_version: str
    explanation: str
    left_version_id: UUID
    right_version_id: UUID
    row_id: UUID
    score: Decimal


SQL = """-- 近似レシピ関係を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.recipe_similarity AS t (
    id,
    left_version_id,
    right_version_id,
    algorithm_version,
    score,
    explanation
)
VALUES (
    %(row_id)s,
    %(left_version_id)s,
    %(right_version_id)s,
    %(algorithm_version)s,
    %(score)s,
    %(explanation)s
)
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
        "explanation": values["explanation"],
        "left_version_id": values["left_version_id"],
        "right_version_id": values["right_version_id"],
        "row_id": values["row_id"],
        "score": values["score"],
    }
    return list(connection.execute(SQL, params).fetchall())
