# app-docs による自動生成。直接編集しない。
# SQLのSHA256: d2fa642225748bf955a9a8dc26c111286aa9fa1747ded61275070e6cd10ee4bc
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 認証主体から決定的に採番した本人行を初回だけ作る。
INSERT INTO recipeweave.app_user (id, auth_subject, state, locale, timezone)
VALUES (%(user_id)s, %(subject)s, 'active', 'ja', 'Asia/Tokyo')
ON CONFLICT (auth_subject) DO NOTHING
RETURNING id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("subject", "user_id")}


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
