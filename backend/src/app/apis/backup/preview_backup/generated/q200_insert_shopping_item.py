# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 9a3ce297734d5c68e7fa233916faaf3d14b2ce6f8b5bc609404eedd3dc25ff25
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの買い物行を元IDと全列で復元する。
INSERT INTO recipeweave.shopping_item (
    id,
    created_at,
    session_id,
    total_id,
    product_version_id,
    net_shortage,
    package_count,
    surplus_amount,
    checked,
    client_key,
    checked_at,
    archived
) VALUES (
    %(id)s,
    %(created_at)s,
    %(session_id)s,
    %(total_id)s,
    %(product_version_id)s,
    %(net_shortage)s,
    %(package_count)s,
    %(surplus_amount)s,
    %(checked)s,
    %(client_key)s,
    %(checked_at)s,
    %(archived)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "archived",
        "checked",
        "checked_at",
        "client_key",
        "created_at",
        "id",
        "net_shortage",
        "package_count",
        "product_version_id",
        "session_id",
        "surplus_amount",
        "total_id",
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
