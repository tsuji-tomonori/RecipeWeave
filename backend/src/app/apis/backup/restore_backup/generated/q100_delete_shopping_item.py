# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 56d08128e320d50c9aadffe0b74734f67068a14e38b37aa00693781b4db0cc62
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 全置換の確認対象である本人の買い物行だけを削除する。
DELETE FROM recipeweave.shopping_item AS t
WHERE (EXISTS (
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
));
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("actor_id",)}


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
