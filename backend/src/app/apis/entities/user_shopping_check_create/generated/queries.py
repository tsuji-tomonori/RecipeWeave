# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    amount: Decimal | None
    archived: bool
    checked_at: datetime | None
    food_id: UUID | None
    key: str
    row_id: UUID
    signature: str
    unit_id: UUID | None
    user_id: UUID


SQL = """-- 調理前の買い物確認を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.user_shopping_check AS t (
    id,
    user_id,
    key,
    signature,
    food_id,
    amount,
    unit_id,
    checked_at,
    archived
)
VALUES (
    %(row_id)s,
    %(user_id)s,
    %(key)s,
    %(signature)s,
    %(food_id)s,
    %(amount)s,
    %(unit_id)s,
    %(checked_at)s,
    %(archived)s
)
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
        "amount": values["amount"],
        "archived": values["archived"],
        "checked_at": values["checked_at"],
        "food_id": values["food_id"],
        "key": values["key"],
        "row_id": values["row_id"],
        "signature": values["signature"],
        "unit_id": values["unit_id"],
        "user_id": values["user_id"],
    }
    return list(connection.execute(SQL, params).fetchall())
