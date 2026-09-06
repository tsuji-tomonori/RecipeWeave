# app-docs による自動生成。直接編集しない。
# SQLのSHA256: b0e15aa8ed17d26d29be7eae1a11d6f8d5b5e0750e075697605b72e3a90910a9
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 本人の言語とタイムゾーンだけを復元し、認証主体とアカウント状態は保持する。
UPDATE recipeweave.app_user SET locale = %(locale)s, timezone = %(timezone)s
WHERE id = %(actor_id)s;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("actor_id", "locale", "timezone")}


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
