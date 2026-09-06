# app-docs による自動生成。直接編集しない。
# SQLのSHA256: f00ce29801482be5cde208a41ae0cb11e84d26e98da73514c26d14e918007823
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの商品仕様版を元IDと全列で復元する。
INSERT INTO recipeweave.product_version (
    id,
    created_at,
    product_id,
    version,
    form_id,
    net_amount,
    unit_id,
    drain_amount,
    source_id,
    preparation_note,
    valid_from
) VALUES (
    %(id)s,
    %(created_at)s,
    %(product_id)s,
    %(version)s,
    %(form_id)s,
    %(net_amount)s,
    %(unit_id)s,
    %(drain_amount)s,
    %(source_id)s,
    %(preparation_note)s,
    %(valid_from)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "created_at",
        "drain_amount",
        "form_id",
        "id",
        "net_amount",
        "preparation_note",
        "product_id",
        "source_id",
        "unit_id",
        "valid_from",
        "version",
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
