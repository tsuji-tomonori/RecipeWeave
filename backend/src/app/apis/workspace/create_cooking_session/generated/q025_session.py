# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 00781c3bdc066d31fd235d397d3d4d2055742e55d14bf50227f217a9e4aaa1c7
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 正規化した入力行の識別子・固定量だけを版付き入力契約へ保存する。
INSERT INTO recipeweave.cooking_session
(id, menu_id, menu_revision, status, target_at, planner_version, input_snapshot, input_hash)
VALUES (
    %(session_id)s,
    %(menu_id)s,
    %(revision)s,
    'cooking',
    NULL,
    'dag-resource-v1',
    %(snapshot)s,
    %(hash)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("hash", "menu_id", "revision", "session_id", "snapshot")
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
