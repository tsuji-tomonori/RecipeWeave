# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 9929e63497ce75ba24b99fbcb80ad91d757a64ff558a98da4eb3e2d04ce75f7a
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの献立別材料確定を元IDと全列で復元する。
INSERT INTO recipeweave.menu_ingredient_override (
    id,
    created_at,
    menu_item_id,
    ingredient_line_id,
    selected,
    amount,
    form_id,
    product_version_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(menu_item_id)s,
    %(ingredient_line_id)s,
    %(selected)s,
    %(amount)s,
    %(form_id)s,
    %(product_version_id)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "amount",
        "created_at",
        "form_id",
        "id",
        "ingredient_line_id",
        "menu_item_id",
        "product_version_id",
        "selected",
    )
}


def _execute(
    connection: Connection[dict[str, Any]], name: str, params: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """許可された固定SQLだけに、宣言と一致する束縛値を別渡しする。"""
    if name not in QUERIES or set(params) != set(PARAMETERS[name]):
        raise ValueError("SQL名または束縛パラメータが操作契約にありません")
    cursor = connection.execute(QUERIES[name], dict(params))
    return list(cursor.fetchall()) if cursor.description is not None else []


SQL = QUERIES["query"]


def execute(
    connection: Connection[dict[str, Any]], values: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """固定した単文SQLを実行する。"""
    return _execute(connection, "query", values)
