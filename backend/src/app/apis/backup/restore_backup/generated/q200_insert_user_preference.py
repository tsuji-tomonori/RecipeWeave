# app-docs による自動生成。直接編集しない。
# SQLのSHA256: f59939725d1999d158c70fbf795e141e8a8528721e59540005913f491947f824
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップのユーザーの嗜好を元IDと全列で復元する。
INSERT INTO recipeweave.user_preference (
    id,
    created_at,
    user_id,
    option_id,
    weight
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(option_id)s,
    %(weight)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": ("created_at", "id", "option_id", "user_id", "weight")
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
