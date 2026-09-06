# app-docs による自動生成。直接編集しない。
# SQLのSHA256: d99f03a815c631bde6930cfe65f7c93920f31d65a403826f6214efa05e413b21
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 設定集合は物理行順を使わず、種類・値の固定順で返す。
WITH settings AS (
    SELECT
        'excluded' AS kind,
        food_id::TEXT AS setting_value
    FROM recipeweave.user_exclusion
    WHERE user_id = %(user_id)s AND food_id IS NOT NULL
    UNION ALL
    SELECT
        'pantry' AS kind,
        food_id::TEXT AS setting_value
    FROM recipeweave.user_pantry_food
    WHERE user_id = %(user_id)s
    UNION ALL
    SELECT
        'equipment' AS kind,
        r.name AS setting_value
    FROM recipeweave.kitchen_resource AS k
    INNER JOIN recipeweave.resource_type AS r ON k.resource_type_id = r.id
    WHERE k.user_id = %(user_id)s AND k.active AND r.code NOT IN ('person', 'burner', 'bowl')
)

SELECT
    settings.kind,
    settings.setting_value
FROM settings
ORDER BY settings.kind, CONVERT_TO(settings.setting_value, 'UTF8');
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
