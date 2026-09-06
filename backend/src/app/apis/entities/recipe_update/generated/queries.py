# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    expected_etag: str
    family_option_id: UUID
    row_id: UUID
    status: str
    title: str
    withdrawal_reason: str | None


SQL = """-- レシピ同一性を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.recipe AS t
SET
    title = %(title)s,
    family_option_id = %(family_option_id)s,
    status = %(status)s,
    withdrawal_reason = %(withdrawal_reason)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
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
        "expected_etag": values["expected_etag"],
        "family_option_id": values["family_option_id"],
        "row_id": values["row_id"],
        "status": values["status"],
        "title": values["title"],
        "withdrawal_reason": values["withdrawal_reason"],
    }
    return list(connection.execute(SQL, params).fetchall())
