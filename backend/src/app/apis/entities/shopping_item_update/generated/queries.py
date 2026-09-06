# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    archived: bool
    checked: bool
    checked_at: datetime | None
    client_key: str | None
    expected_etag: str
    net_shortage: Decimal
    package_count: int | None
    product_version_id: UUID | None
    row_id: UUID
    session_id: UUID
    surplus_amount: Decimal | None
    total_id: UUID


SQL = """-- 買い物行を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.shopping_item AS t
SET
    session_id = %(session_id)s,
    total_id = %(total_id)s,
    product_version_id = %(product_version_id)s,
    net_shortage = %(net_shortage)s,
    package_count = %(package_count)s,
    surplus_amount = %(surplus_amount)s,
    checked = %(checked)s,
    client_key = %(client_key)s,
    checked_at = %(checked_at)s,
    archived = %(archived)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND EXISTS (
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
RETURNING
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
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "actor_id": values["actor_id"],
        "archived": values["archived"],
        "checked": values["checked"],
        "checked_at": values["checked_at"],
        "client_key": values["client_key"],
        "expected_etag": values["expected_etag"],
        "net_shortage": values["net_shortage"],
        "package_count": values["package_count"],
        "product_version_id": values["product_version_id"],
        "row_id": values["row_id"],
        "session_id": values["session_id"],
        "surplus_amount": values["surplus_amount"],
        "total_id": values["total_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
