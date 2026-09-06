# generate_entity_apis.py による自動生成。直接編集しない。
from collections.abc import Mapping
from decimal import Decimal
from typing import Any, TypedDict
from uuid import UUID

from psycopg import Connection


class Parameters(TypedDict):
    amount: Decimal | None
    form_id: UUID | None
    ingredient_line_id: UUID
    menu_item_id: UUID
    product_version_id: UUID | None
    row_id: UUID
    selected: bool


SQL = """-- 献立別材料確定を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.menu_ingredient_override AS t (
    id,
    menu_item_id,
    ingredient_line_id,
    selected,
    amount,
    form_id,
    product_version_id
)
VALUES (
    %(row_id)s,
    %(menu_item_id)s,
    %(ingredient_line_id)s,
    %(selected)s,
    %(amount)s,
    %(form_id)s,
    %(product_version_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.menu_item_id,
    t.ingredient_line_id,
    t.selected,
    t.amount,
    t.form_id,
    t.product_version_id,
    t.xmin::TEXT AS etag;
"""


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """宣言済みパラメータだけをSQLへ束縛して明示列を返す。"""
    params: Parameters = {
        "amount": values["amount"],
        "form_id": values["form_id"],
        "ingredient_line_id": values["ingredient_line_id"],
        "menu_item_id": values["menu_item_id"],
        "product_version_id": values["product_version_id"],
        "row_id": values["row_id"],
        "selected": values["selected"],
    }
    return list(connection.execute(SQL, params).fetchall())
