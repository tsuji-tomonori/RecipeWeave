# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import datetime
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    content_hash: str | None
    expected_etag: str
    license_note: str | None
    locator: str | None
    retrieved_at: datetime | None
    row_id: UUID
    title: str
    url: str | None


SQL = """-- 根拠資料を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.source_record AS t
SET
    title = %(title)s,
    url = %(url)s,
    locator = %(locator)s,
    retrieved_at = %(retrieved_at)s,
    content_hash = %(content_hash)s,
    license_note = %(license_note)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
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
        "expected_etag": values["expected_etag"],
        "license_note": values["license_note"],
        "locator": values["locator"],
        "retrieved_at": values["retrieved_at"],
        "row_id": values["row_id"],
        "title": values["title"],
        "url": values["url"],
    }
    return list(connection.execute(SQL, params).fetchall())
