# app-docs による自動生成。直接編集しない。
# SQLのSHA256: af108757889088ab842e5054118836464d81dd5da5c1f6d7b804d88bf9930e78
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 全置換の確認対象である本人の処理歩留まりだけを削除する。
DELETE FROM recipeweave.form_yield AS t
WHERE
    (EXISTS (
        SELECT 1
        FROM recipeweave.food AS food
        INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id
        WHERE form.id = t.input_form_id AND food.owner_id = %(actor_id)s
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
