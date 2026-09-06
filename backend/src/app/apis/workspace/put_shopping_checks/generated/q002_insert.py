# app-docs による自動生成。直接編集しない。
# SQLのSHA256: d62cc746f0d8ffdac9b25b6d147f15b38df645bf0be3a1b27cf064cd2a6110fa
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 食品と単位を参照して、数量不明を含む購入確認を保存する。
INSERT INTO recipeweave.user_shopping_check (
    id, user_id, key, signature, food_id, amount, unit_id, checked_at, archived
)
SELECT
    %(row_id)s,
    %(user_id)s,
    %(key)s,
    %(signature)s,
    %(food_id)s,
    %(amount)s,
    u.id,
    %(checked_at)s,
    %(archived)s
FROM recipeweave.unit AS u
WHERE u.code = %(unit)s AND u.status = 'active' RETURNING id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "amount",
        "archived",
        "checked_at",
        "food_id",
        "key",
        "row_id",
        "signature",
        "unit",
        "user_id",
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
