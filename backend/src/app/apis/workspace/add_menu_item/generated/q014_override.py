# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 063c035974dddd3b6a6520c02a39d23acee182fd7d6764586fd5013b2d51944f
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 利用者が確認した確定分量だけを元の材料行へ結び付ける。
INSERT INTO recipeweave.menu_ingredient_override (
    id, menu_item_id, ingredient_line_id, selected, amount, form_id, product_version_id
)
VALUES (%(row_id)s, %(item_id)s, %(ingredient_id)s, %(selected)s, %(amount)s, NULL, NULL);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("amount", "ingredient_id", "item_id", "row_id", "selected")
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
