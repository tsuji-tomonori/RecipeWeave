# app-docs による自動生成。直接編集しない。
# SQLのSHA256: d9bd5d33ec5dc62c4063d46a49707df06491dc7236f19859bd8bd0af04649187
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 現在の買い物確認を本人の範囲で置き換える。
DELETE FROM recipeweave.user_shopping_check
WHERE user_id = %(user_id)s;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("user_id",)}


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
