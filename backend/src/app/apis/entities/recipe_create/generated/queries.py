# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    family_option_id: UUID
    row_id: UUID
    status: str
    title: str
    withdrawal_reason: str | None


SQL = """-- レシピ同一性を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.recipe AS t (
    id,
    title,
    family_option_id,
    status,
    withdrawal_reason
)
VALUES (
    %(row_id)s,
    %(title)s,
    %(family_option_id)s,
    %(status)s,
    %(withdrawal_reason)s
)
RETURNING
    t.id,
    t.created_at,
    t.title,
    t.family_option_id,
    t.status,
    t.withdrawal_reason,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "family_option_id": values["family_option_id"],
        "row_id": values["row_id"],
        "status": values["status"],
        "title": values["title"],
        "withdrawal_reason": values["withdrawal_reason"],
    }
    return list(connection.execute(SQL, params).fetchall())
