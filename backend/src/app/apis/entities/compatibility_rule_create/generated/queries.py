# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection
from psycopg.types.json import Jsonb


class Parameters(TypedDict):
    code: str
    message: str
    predicate: Jsonb
    row_id: UUID
    severity: str
    source_id: UUID | None
    status: str
    version: int


SQL = """-- 組み合わせ・公開ルールを作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.compatibility_rule AS t (
    id,
    code,
    version,
    severity,
    predicate,
    message,
    source_id,
    status
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(version)s,
    %(severity)s,
    %(predicate)s,
    %(message)s,
    %(source_id)s,
    %(status)s
)
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.version,
    t.severity,
    t.predicate,
    t.message,
    t.source_id,
    t.status,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "code": values["code"],
        "message": values["message"],
        "predicate": values["predicate"],
        "row_id": values["row_id"],
        "severity": values["severity"],
        "source_id": values["source_id"],
        "status": values["status"],
        "version": values["version"],
    }
    return list(connection.execute(SQL, params).fetchall())
