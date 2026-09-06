# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 734629f0d3495d28399e1cc2478e01d000a39462ce262f3cf4e93a0735fd7a31
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 検証済みバックアップの手持ち食材ロットを元IDと全列で復元する。
INSERT INTO recipeweave.pantry_lot (
    id,
    created_at,
    user_id,
    form_id,
    product_version_id,
    amount,
    unit_id,
    expires_on,
    opened_at,
    location,
    priority,
    status,
    source_import_id,
    quantity_quality,
    original_form_id,
    original_amount,
    original_unit_id,
    updated_at,
    edited
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(form_id)s,
    %(product_version_id)s,
    %(amount)s,
    %(unit_id)s,
    %(expires_on)s,
    %(opened_at)s,
    %(location)s,
    %(priority)s,
    %(status)s,
    %(source_import_id)s,
    %(quantity_quality)s,
    %(original_form_id)s,
    %(original_amount)s,
    %(original_unit_id)s,
    %(updated_at)s,
    %(edited)s
);
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "amount",
        "created_at",
        "edited",
        "expires_on",
        "form_id",
        "id",
        "location",
        "opened_at",
        "original_amount",
        "original_form_id",
        "original_unit_id",
        "priority",
        "product_version_id",
        "quantity_quality",
        "source_import_id",
        "status",
        "unit_id",
        "updated_at",
        "user_id",
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
