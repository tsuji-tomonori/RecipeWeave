# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    actor_id: UUID
    amount: Decimal | None
    archived: bool
    checked_at: datetime | None
    expected_etag: str
    food_id: UUID | None
    key: str
    row_id: UUID
    signature: str
    unit_id: UUID | None
    user_id: UUID


SQL = """-- 調理前の買い物確認を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.user_shopping_check AS t
SET
    user_id = %(user_id)s,
    key = %(key)s,
    signature = %(signature)s,
    food_id = %(food_id)s,
    amount = %(amount)s,
    unit_id = %(unit_id)s,
    checked_at = %(checked_at)s,
    archived = %(archived)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND t.user_id = %(actor_id)s
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.key,
    t.signature,
    t.food_id,
    t.amount,
    t.unit_id,
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
        "amount": values["amount"],
        "archived": values["archived"],
        "checked_at": values["checked_at"],
        "expected_etag": values["expected_etag"],
        "food_id": values["food_id"],
        "key": values["key"],
        "row_id": values["row_id"],
        "signature": values["signature"],
        "unit_id": values["unit_id"],
        "user_id": values["user_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
