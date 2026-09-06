# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 80c1fc3305db0143b0db3f6585240eecf8e16f116bb6a443c2f352236fea576b
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 私有カタログへ本人の独自食材を登録する。
INSERT INTO recipeweave.food (id, code, name, kind, parent_id, release_id, status, owner_id)
VALUES (
    %(food_id)s, %(code)s, %(name)s, 'basic', NULL, %(release_id)s, 'active', %(user_id)s
) RETURNING id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("code", "food_id", "name", "release_id", "user_id")
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
