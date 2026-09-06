# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 87ca137f255f586bd1ce4b1d1177a4165d44d8f02b0157c5dfbaa82b2117182c
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 全置換の確認対象である本人の形態・商品別栄養値だけを削除する。
DELETE FROM recipeweave.nutrition_fact AS t
WHERE
    (
        EXISTS (
            SELECT 1
            FROM recipeweave.food AS food
            INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id
            WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s
        )
        OR EXISTS (
            SELECT 1
            FROM recipeweave.food AS food
            INNER JOIN recipeweave.product AS product ON food.id = product.food_id
            INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id
            WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s
        )
    );
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
