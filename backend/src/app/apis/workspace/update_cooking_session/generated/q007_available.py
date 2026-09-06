# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 75cd65561911bb1f6dbc6eed0fc23b13d9ba8f5281305046f6bb16927a59891f
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 同じ形態・単位の確定数量だけを期限と登録順で消費候補にする。
SELECT
    id,
    amount
FROM recipeweave.pantry_lot
WHERE
    user_id = %(user_id)s AND form_id = %(form_id)s AND unit_id = %(unit_id)s
    AND product_version_id IS NOT DISTINCT FROM %(product_id)s
    AND status = 'active' AND quantity_quality = 'known' AND amount > 0
ORDER BY expires_on NULLS LAST, created_at, id FOR UPDATE;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("form_id", "product_id", "unit_id", "user_id")}


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
