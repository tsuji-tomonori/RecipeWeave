# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import datetime
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    content_hash: str | None
    license_note: str | None
    locator: str | None
    retrieved_at: datetime | None
    row_id: UUID
    title: str
    url: str | None


SQL = """-- 根拠資料を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.source_record AS t (
    id,
    title,
    url,
    locator,
    retrieved_at,
    content_hash,
    license_note
)
VALUES (
    %(row_id)s,
    %(title)s,
    %(url)s,
    %(locator)s,
    %(retrieved_at)s,
    %(content_hash)s,
    %(license_note)s
)
RETURNING
    t.id,
    t.created_at,
    t.title,
    t.url,
    t.locator,
    t.retrieved_at,
    t.content_hash,
    t.license_note,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "content_hash": values["content_hash"],
        "license_note": values["license_note"],
        "locator": values["locator"],
        "retrieved_at": values["retrieved_at"],
        "row_id": values["row_id"],
        "title": values["title"],
        "url": values["url"],
    }
    return list(connection.execute(SQL, params).fetchall())
