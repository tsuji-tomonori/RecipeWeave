# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    end_ms: int
    expected_etag: str
    media_id: UUID
    row_id: UUID
    start_ms: int
    step_id: UUID


SQL = """-- 工程別メディア選択を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.step_media AS t
SET
    step_id = %(step_id)s,
    media_id = %(media_id)s,
    start_ms = %(start_ms)s,
    end_ms = %(end_ms)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.step_id,
    t.media_id,
    t.start_ms,
    t.end_ms,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "end_ms": values["end_ms"],
        "expected_etag": values["expected_etag"],
        "media_id": values["media_id"],
        "row_id": values["row_id"],
        "start_ms": values["start_ms"],
        "step_id": values["step_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
