# app-docs による自動生成。直接編集しない。
# SQLのSHA256: fa7a63f0126e3da9d7412f88db22be6600619e7509dd0cf7732bccd18c6b839d
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 本人の編集可能なロットだけを更新し、取消済みレシートの在庫は復元しない。
UPDATE recipeweave.pantry_lot AS p SET
    form_id = %(form_id)s, amount = %(amount)s,
    unit_id = %(unit_id)s, expires_on = %(expires_on)s, location = %(location)s,
    priority = %(priority)s, quantity_quality = %(quality)s, status = 'active',
    updated_at = CURRENT_TIMESTAMP, edited = TRUE
WHERE
    p.id = %(row_id)s AND p.user_id = %(user_id)s
    AND (p.status = 'active' OR (p.status = 'deleted' AND %(restore)s))
    AND NOT EXISTS (
        SELECT 1 FROM recipeweave.receipt_import AS r
        WHERE r.id = p.source_import_id AND r.status = 'reverted'
    )
RETURNING p.id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "amount",
        "expires_on",
        "form_id",
        "location",
        "priority",
        "quality",
        "restore",
        "row_id",
        "unit_id",
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
