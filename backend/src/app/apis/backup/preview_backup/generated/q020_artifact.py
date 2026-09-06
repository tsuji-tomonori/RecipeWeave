# app-docs による自動生成。直接編集しない。
# SQLのSHA256: b9c8654dc89a48abfcefb7739c1e61d0ba399e82ff618c4f89cc25ea62716066
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 発行した本人と本文digestが一致する根拠だけを認可に使う。
SELECT id FROM recipeweave.backup_artifact
WHERE
    id = %(artifact_id)s AND user_id = %(actor_id)s
    AND body_sha256 = %(body_sha256)s AND format_version = 2;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("actor_id", "artifact_id", "body_sha256")}


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
