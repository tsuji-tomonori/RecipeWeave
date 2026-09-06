# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 6853dafe5568b3bcc255c8b3534a5b621e903cfb08823cea481c3d549523a64e
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 予約履歴が参照する設備IDを保持し、画面で選択する器具だけを無効にする。
UPDATE recipeweave.kitchen_resource AS k SET active = FALSE
WHERE k.user_id = %(user_id)s AND EXISTS (SELECT 1 FROM recipeweave.resource_type AS r
WHERE r.id = k.resource_type_id AND r.code NOT IN ('person', 'burner', 'bowl'));
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("user_id",)}


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
