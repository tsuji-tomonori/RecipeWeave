# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 6eee3b93a52dc8ad30be9b0ddba407b44e0c80a99999616ef69f600801adabe7
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 現在の献立を初回だけ作成し、所有者を固定する。
INSERT INTO recipeweave.menu (id, user_id, name, servings, revision)
VALUES (%(menu_id)s, %(user_id)s, %(name)s, 2, 1) ON CONFLICT (id) DO NOTHING;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("menu_id", "name", "user_id")}


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
