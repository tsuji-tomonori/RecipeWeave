# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import datetime
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    end_ordinal: int
    fence_token: int
    lease_expires_at: datetime | None
    lease_owner: str | None
    next_ordinal: int
    row_id: UUID
    start_ordinal: int
    state: str
    template_id: UUID


SQL = """-- 列挙範囲・リース管理を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.generation_shard AS t (
    id,
    template_id,
    start_ordinal,
    end_ordinal,
    next_ordinal,
    lease_owner,
    lease_expires_at,
    fence_token,
    state
)
VALUES (
    %(row_id)s,
    %(template_id)s,
    %(start_ordinal)s,
    %(end_ordinal)s,
    %(next_ordinal)s,
    %(lease_owner)s,
    %(lease_expires_at)s,
    %(fence_token)s,
    %(state)s
)
RETURNING
    t.id,
    t.created_at,
    t.template_id,
    t.start_ordinal,
    t.end_ordinal,
    t.next_ordinal,
    t.lease_owner,
    t.lease_expires_at,
    t.fence_token,
    t.state,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "end_ordinal": values["end_ordinal"],
        "fence_token": values["fence_token"],
        "lease_expires_at": values["lease_expires_at"],
        "lease_owner": values["lease_owner"],
        "next_ordinal": values["next_ordinal"],
        "row_id": values["row_id"],
        "start_ordinal": values["start_ordinal"],
        "state": values["state"],
        "template_id": values["template_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
