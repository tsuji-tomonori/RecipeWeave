# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 9b5e1b93cbed61140e86c5d3a04c9a26bdb66a3f1b7c2d14040abcfaf8ae224a
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 全置換の確認対象である本人の献立の料理だけを削除する。
DELETE FROM recipeweave.menu_item AS t
WHERE (EXISTS (
    SELECT owner_0.id
    FROM recipeweave.menu AS owner_0
    WHERE
        owner_0.id = t.menu_id
        AND owner_0.user_id = %(actor_id)s
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
