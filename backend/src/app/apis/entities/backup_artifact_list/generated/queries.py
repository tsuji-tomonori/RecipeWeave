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
    "-- 本人へ発行したバックアップの証拠。本文を保存せず、削除後も匿名化し"
    "た発行記録を保持するを一覧取得する。\n"
    "-- 値は名前付きパラメータで束縛する。\n"
    "SELECT\n"
    "    t.id,\n"
    "    t.created_at,\n"
    "    t.user_id,\n"
    "    t.body_sha256,\n"
    "    t.format_version,\n"
    "    t.xmin::TEXT AS etag\n"
    "FROM recipeweave.backup_artifact AS t\n"
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
