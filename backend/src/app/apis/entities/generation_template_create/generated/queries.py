# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection
from psycopg.types.json import Jsonb


class Parameters(TypedDict):
    candidate_count: int
    code: str
    contract: Jsonb
    contract_hash: str
    release_id: UUID
    row_id: UUID
    version: int


SQL = """-- 列挙テンプレート版を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.generation_template AS t (
    id,
    code,
    version,
    release_id,
    contract,
    candidate_count,
    contract_hash
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(version)s,
    %(release_id)s,
    %(contract)s,
    %(candidate_count)s,
    %(contract_hash)s
)
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.version,
    t.release_id,
    t.contract,
    t.candidate_count,
    t.contract_hash,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "candidate_count": values["candidate_count"],
        "code": values["code"],
        "contract": values["contract"],
        "contract_hash": values["contract_hash"],
        "release_id": values["release_id"],
        "row_id": values["row_id"],
        "version": values["version"],
    }
    return list(connection.execute(SQL, params).fetchall())
