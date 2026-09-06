# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    after_id: UUID | None
    page_limit: int


SQL = """-- 買い物行を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.session_id,
    t.total_id,
    t.product_version_id,
    t.net_shortage,
    t.package_count,
    t.surplus_amount,
    t.checked,
    t.client_key,
    t.checked_at,
    t.archived,
    t.xmin::TEXT AS etag
FROM recipeweave.shopping_item AS t
WHERE
    EXISTS (
        SELECT owner_0.id
        FROM recipeweave.cooking_session AS owner_0
        WHERE
            owner_0.id = t.session_id
            AND EXISTS (
                SELECT owner_1.id
                FROM recipeweave.menu AS owner_1
                WHERE
                    owner_1.id = owner_0.menu_id
                    AND owner_1.user_id = %(actor_id)s
            )
    )
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
"""


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
