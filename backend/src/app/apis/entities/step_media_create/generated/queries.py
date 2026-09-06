# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    end_ms: int
    media_id: UUID
    row_id: UUID
    start_ms: int
    step_id: UUID


SQL = """-- 工程別メディア選択を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.step_media AS t (
    id,
    step_id,
    media_id,
    start_ms,
    end_ms
)
VALUES (
    %(row_id)s,
    %(step_id)s,
    %(media_id)s,
    %(start_ms)s,
    %(end_ms)s
)
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
        "media_id": values["media_id"],
        "row_id": values["row_id"],
        "start_ms": values["start_ms"],
        "step_id": values["step_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
