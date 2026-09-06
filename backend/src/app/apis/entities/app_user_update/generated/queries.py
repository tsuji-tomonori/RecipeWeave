# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    expected_etag: str
    locale: str
    row_id: UUID
    timezone: str


SQL = """-- アプリ利用者を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.app_user AS t
SET
    locale = %(locale)s,
    timezone = %(timezone)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND t.id = %(actor_id)s
RETURNING
    t.id,
    t.created_at,
    t.auth_subject,
    t.state,
    t.locale,
    t.timezone,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "actor_id": values["actor_id"],
        "expected_etag": values["expected_etag"],
        "locale": values["locale"],
        "row_id": values["row_id"],
        "timezone": values["timezone"],
    }
    return list(connection.execute(SQL, params).fetchall())
