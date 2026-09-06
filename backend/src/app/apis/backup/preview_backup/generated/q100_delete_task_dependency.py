# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 8157207df1ff85c0f600177ef8dbb367369b47a1b6d52a02a18e1f9327599175
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 全置換の確認対象である本人の献立展開後依存だけを削除する。
DELETE FROM recipeweave.task_dependency AS t
WHERE (EXISTS (
    SELECT owner_0.id
    FROM recipeweave.session_task AS owner_0
    WHERE
        owner_0.id = t.before_task_id
        AND EXISTS (
            SELECT owner_1.id
            FROM recipeweave.cooking_session AS owner_1
            WHERE
                owner_1.id = owner_0.session_id
                AND EXISTS (
                    SELECT owner_2.id
                    FROM recipeweave.menu AS owner_2
                    WHERE
                        owner_2.id = owner_1.menu_id
                        AND owner_2.user_id = %(actor_id)s
                )
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
