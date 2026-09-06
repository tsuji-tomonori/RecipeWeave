# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    after_id: UUID | None
    page_limit: int


SQL = (
    "-- 復元内容の確認記録。本人・本文・確認時の更新版・期限を固定し、一度"
    "だけ消費するを一覧取得する。\n"
    "-- 値は名前付きパラメータで束縛する。\n"
    "SELECT\n"
    "    t.id,\n"
    "    t.created_at,\n"
    "    t.user_id,\n"
    "    t.artifact_id,\n"
    "    t.body_sha256,\n"
    "    t.current_revision,\n"
    "    t.expires_at,\n"
    "    t.consumed_at,\n"
    "    t.xmin::TEXT AS etag\n"
    "FROM recipeweave.backup_restore_intent AS t\n"
    "WHERE\n"
    "    t.user_id = %(actor_id)s\n"
    "    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)\n"
    "ORDER BY t.id\n"
    "LIMIT %(page_limit)s;\n"
)


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "actor_id": values["actor_id"],
        "after_id": values["after_id"],
        "page_limit": values["page_limit"],
    }
    return list(connection.execute(SQL, params).fetchall())
