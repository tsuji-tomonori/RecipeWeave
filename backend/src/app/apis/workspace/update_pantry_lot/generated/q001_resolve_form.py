# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 95e901428a70edd6cf5331a8b460146875bbacd9411e9570bb7dd255cf67226e
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """-- 食材形態と単位をDBから検証し、他人の独自食材は参照させない。
SELECT
    fm.id AS form_id,
    u.id AS unit_id
FROM recipeweave.food_form AS fm
INNER JOIN recipeweave.food AS f ON fm.food_id = f.id
CROSS JOIN recipeweave.unit AS u
WHERE
    fm.food_id = %(food_id)s AND fm.name = %(form)s AND fm.status = 'active'
    AND u.code = %(unit)s AND u.status = 'active'
    AND (
        NOT EXISTS (
            SELECT 1 FROM recipeweave.user_food AS own
            WHERE own.food_id = f.id
        )
        OR EXISTS (
            SELECT 1 FROM recipeweave.user_food AS own
            WHERE own.food_id = f.id AND own.user_id = %(user_id)s
        )
    )
ORDER BY fm.id LIMIT 1;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("food_id", "form", "unit", "user_id")}


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
