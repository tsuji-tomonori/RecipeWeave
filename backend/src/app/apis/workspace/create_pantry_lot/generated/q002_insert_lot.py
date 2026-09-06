# app-docs による自動生成。直接編集しない。
# SQLのSHA256: d9ee914fbe437c2954cfc81cfd9b111b5ccb933f8a2a5b20b0af66ffca3d2908
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 登録時の値と現在値を一緒に記録する。不明数量はNULLのまま保持する。
INSERT INTO recipeweave.pantry_lot
(
    id, user_id, form_id, amount, unit_id, expires_on, location, priority, source_import_id,
    quantity_quality, original_form_id, original_amount, original_unit_id
)
VALUES (
    %(row_id)s, %(user_id)s, %(form_id)s, %(amount)s, %(unit_id)s, %(expires_on)s,
    %(location)s, %(priority)s, %(import_id)s, %(quality)s, %(form_id)s, %(amount)s, %(unit_id)s
)
RETURNING id;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {
    "query": (
        "amount",
        "expires_on",
        "form_id",
        "import_id",
        "location",
        "priority",
        "quality",
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
