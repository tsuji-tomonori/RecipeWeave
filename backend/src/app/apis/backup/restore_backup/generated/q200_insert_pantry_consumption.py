# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 016dea80bb179b36f08dce4ab92c94c7108cf5841529820fa7de70e944003aff
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの調理による在庫消費の冪等台帳を元IDと全列で復元する。
INSERT INTO recipeweave.pantry_consumption (
    id,
    created_at,
    user_id,
    session_id,
    lot_id,
    amount,
    unit_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(session_id)s,
    %(lot_id)s,
    %(amount)s,
    %(unit_id)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("amount", "created_at", "id", "lot_id", "session_id", "unit_id", "user_id")
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
