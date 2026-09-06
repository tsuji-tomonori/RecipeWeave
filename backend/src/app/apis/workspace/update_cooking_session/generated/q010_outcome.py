# app-docs による自動生成。直接編集しない。
# SQLのSHA256: e04d8c790f4f7fade76c1af53dea02351c16913dcaaf47be32dca6a9a936a259
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 計画量を上書きせず、実際に確認した使用量と適用結果を保存する。
UPDATE recipeweave.ingredient_total SET
    actual_amount = %(amount)s, consumption_outcome = %(outcome)s
WHERE id = %(total_id)s AND session_id = %(session_id)s;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("amount", "outcome", "session_id", "total_id")}


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
