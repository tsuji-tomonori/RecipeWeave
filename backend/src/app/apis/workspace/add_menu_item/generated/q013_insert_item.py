# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 6c4e0b2865320957ec04c0e87cba4d0a694a3baea1e526633895d731955822f4
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 検証した料理版と人数を献立へ登録する。
INSERT INTO recipeweave.menu_item (
    id, menu_id, recipe_version_id, servings, role_option_id, position
)
VALUES (
    %(row_id)s, %(menu_id)s, %(version_id)s, %(servings)s, NULL,
    (
        SELECT COALESCE(MAX(mi.position), 0) + 1 FROM recipeweave.menu_item AS mi
        WHERE mi.menu_id = %(menu_id)s
    )
)
RETURNING id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("menu_id", "row_id", "servings", "version_id")}


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
