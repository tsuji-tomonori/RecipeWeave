# app-docs による自動生成。直接編集しない。
# SQLのSHA256: b6e70b517aaa1232ad887aadb37c3475439e3a9c820353640816851a46de14be
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの献立の料理を元IDと全列で復元する。
INSERT INTO recipeweave.menu_item (
    id,
    created_at,
    menu_id,
    recipe_version_id,
    servings,
    role_option_id,
    position
) VALUES (
    %(id)s,
    %(created_at)s,
    %(menu_id)s,
    %(recipe_version_id)s,
    %(servings)s,
    %(role_option_id)s,
    %(position)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "created_at",
        "id",
        "menu_id",
        "position",
        "recipe_version_id",
        "role_option_id",
        "servings",
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
