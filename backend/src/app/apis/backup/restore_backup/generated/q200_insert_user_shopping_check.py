# app-docs による自動生成。直接編集しない。
# SQLのSHA256: bfa815ee6e75d46f3b0754fa7edf178538337f3ebc54bd88633879926d29a680
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの調理前の買い物確認を元IDと全列で復元する。
INSERT INTO recipeweave.user_shopping_check (
    id,
    created_at,
    user_id,
    key,
    signature,
    food_id,
    amount,
    unit_id,
    checked_at,
    archived
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(key)s,
    %(signature)s,
    %(food_id)s,
    %(amount)s,
    %(unit_id)s,
    %(checked_at)s,
    %(archived)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "amount",
        "archived",
        "checked_at",
        "created_at",
        "food_id",
        "id",
        "key",
        "signature",
        "unit_id",
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
