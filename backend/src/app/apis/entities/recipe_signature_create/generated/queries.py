# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection
from psycopg.types.json import Jsonb


class Parameters(TypedDict):
    algorithm_version: str
    canonical_payload: Jsonb
    cluster_key: str
    exact_hash: str
    recipe_version_id: UUID
    row_id: UUID


SQL = """-- 内容重複判定署名を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.recipe_signature AS t (
    id,
    recipe_version_id,
    algorithm_version,
    exact_hash,
    canonical_payload,
    cluster_key
)
VALUES (
    %(row_id)s,
    %(recipe_version_id)s,
    %(algorithm_version)s,
    %(exact_hash)s,
    %(canonical_payload)s,
    %(cluster_key)s
)
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.algorithm_version,
    t.exact_hash,
    t.canonical_payload,
    t.cluster_key,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "algorithm_version": values["algorithm_version"],
        "canonical_payload": values["canonical_payload"],
        "cluster_key": values["cluster_key"],
        "exact_hash": values["exact_hash"],
        "recipe_version_id": values["recipe_version_id"],
        "row_id": values["row_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
