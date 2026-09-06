# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import datetime
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    manifest_hash: str
    published_at: datetime | None
    row_id: UUID
    version: str


SQL = """-- カタログ公開版を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.catalog_release AS t (
    id,
    version,
    manifest_hash,
    published_at
)
VALUES (
    %(row_id)s,
    %(version)s,
    %(manifest_hash)s,
    %(published_at)s
)
RETURNING
    t.id,
    t.created_at,
    t.version,
    t.manifest_hash,
    t.published_at,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "manifest_hash": values["manifest_hash"],
        "published_at": values["published_at"],
        "row_id": values["row_id"],
        "version": values["version"],
    }
    return list(connection.execute(SQL, params).fetchall())
