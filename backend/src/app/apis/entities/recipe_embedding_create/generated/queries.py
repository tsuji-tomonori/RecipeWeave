# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    content_hash: str
    created_for_index: str
    embedding: list[float]
    model_version: str
    recipe_version_id: UUID
    row_id: UUID


SQL = """-- 近似検索用特徴量を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.recipe_embedding AS t (
    id,
    recipe_version_id,
    model_version,
    content_hash,
    embedding,
    created_for_index
)
VALUES (
    %(row_id)s,
    %(recipe_version_id)s,
    %(model_version)s,
    %(content_hash)s,
    %(embedding)s::VECTOR,
    %(created_for_index)s
)
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.model_version,
    t.content_hash,
    t.embedding,
    t.created_for_index,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "content_hash": values["content_hash"],
        "created_for_index": values["created_for_index"],
        "embedding": values["embedding"],
        "model_version": values["model_version"],
        "recipe_version_id": values["recipe_version_id"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
