# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    row_id: UUID


SQL = """-- 復元内容の確認記録。本人・本文・確認時の更新版・期限を固定し、一度だけ消費するを取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.user_id,
    t.artifact_id,
    t.body_sha256,
    t.current_revision,
    t.expires_at,
    t.consumed_at,
    t.xmin::TEXT AS etag
FROM recipeweave.backup_restore_intent AS t
WHERE
    t.id = %(row_id)s
    AND t.user_id = %(actor_id)s;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {"actor_id": values["actor_id"], "row_id": values["row_id"]}
    return list(connection.execute(SQL, params).fetchall())
