# app-docs による自動生成。直接編集しない。
# SQLのSHA256: ad34c60fe50c5bcbb724ac2f812a3ae385094afa46db9d96e3837f86b3e01d41
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 本人の現在の献立の料理を外す。調理中の入力は専用の献立版へ保存する。
DELETE FROM recipeweave.menu_item
WHERE
    id = %(row_id)s AND menu_id = %(menu_id)s
    AND EXISTS (
        SELECT 1 FROM recipeweave.menu AS m
        WHERE m.id = %(menu_id)s AND m.user_id = %(user_id)s
    )
RETURNING id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("menu_id", "row_id", "user_id")}


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
