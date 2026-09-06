# app-docs による自動生成。直接編集しない。
# SQLのSHA256: ad70bf20fe116835c5fc9969893156918077695a618a0b69e2ed9fba5656e2dc
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの購入・利用食材概念を元IDと全列で復元する。
INSERT INTO recipeweave.food (
    id,
    created_at,
    code,
    name,
    kind,
    parent_id,
    release_id,
    status,
    owner_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(code)s,
    %(name)s,
    %(kind)s,
    %(parent_id)s,
    %(release_id)s,
    %(status)s,
    %(owner_id)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "code",
        "created_at",
        "id",
        "kind",
        "name",
        "owner_id",
        "parent_id",
        "release_id",
        "status",
    )
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
