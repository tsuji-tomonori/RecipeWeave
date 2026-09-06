# app-docs による自動生成。直接編集しない。
# SQLのSHA256: 881760b7a5ab42fd517ef1d368eda1748a5cf53aac60222f1fe6c5e3c2c7ad07
from collections.abc import Mapping
from typing import Any, LiteralString

from psycopg import Connection

QUERIES: dict[str, LiteralString] = {
    "query": """\
-- 正規化した食品・形態・分類・別名から検索用の食品一覧を取得する。
WITH available AS (
    SELECT
        food.id,
        food.name,
        food.kind,
        form.state,
        unit.code AS unit_code,
        COALESCE(aliases.alias_names, '[]'::JSONB) AS aliases,
        COALESCE(attributes.category, 'その他') AS category,
        COALESCE(
            attributes.storage_location,
            CASE
                WHEN form.state = 'frozen' THEN '冷凍'
                WHEN form.state = 'raw' THEN '冷蔵' ELSE '常温'
            END
        ) AS storage_location,
        COALESCE(attributes.pantry, FALSE) AS pantry
    FROM recipeweave.food AS food
    INNER JOIN LATERAL (
        SELECT
            food_form.state,
            food_form.base_unit_id
        FROM recipeweave.food_form AS food_form
        WHERE food_form.food_id = food.id AND food_form.status = 'active'
        ORDER BY (food_form.name = '標準') DESC, food_form.id
        LIMIT 1
    ) AS form ON TRUE
    INNER JOIN recipeweave.unit AS unit ON form.base_unit_id = unit.id
    LEFT JOIN LATERAL (
        SELECT JSONB_AGG(food_alias.alias ORDER BY food_alias.alias) AS alias_names
        FROM recipeweave.food_alias AS food_alias
        WHERE food_alias.food_id = food.id AND food_alias.locale = 'ja'
    ) AS aliases ON TRUE
    LEFT JOIN LATERAL (
        SELECT
            MAX(axis_option.label) FILTER (WHERE axis.code = 'store_category') AS category,
            MAX(axis_option.label) FILTER (WHERE axis.code = 'storage_location')
                AS storage_location,
            BOOL_OR(axis_option.code = 'true') FILTER (WHERE axis.code = 'pantry_default') AS pantry
        FROM recipeweave.food_axis_option AS relation
        INNER JOIN recipeweave.axis_option AS axis_option ON relation.option_id = axis_option.id
        INNER JOIN recipeweave.axis AS axis ON axis_option.axis_id = axis.id
        WHERE relation.food_id = food.id
    ) AS attributes ON TRUE
    WHERE
        food.status = 'active'
        AND (
            %(q)s = '' OR STRPOS(LOWER(food.name), LOWER(%(q)s)) > 0
            OR EXISTS (
                SELECT 1 FROM recipeweave.food_alias AS alias_filter
                WHERE
                    alias_filter.food_id = food.id
                    AND STRPOS(LOWER(alias_filter.alias), LOWER(%(q)s)) > 0
            )
        )
)

SELECT
    COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
        'id', available.id::TEXT,
        'name', available.name,
        'aliases', available.aliases,
        'category', available.category,
        'defaultUnit', available.unit_code,
        'location', available.storage_location,
        'pantry', available.pantry,
        'imageIndex', NULL,
        'componentsKnown', available.kind IN ('basic', 'utility'),
        'componentFoodIds', '[]'::JSONB
    ) ORDER BY available.name, available.id), '[]'::JSONB) AS items,
    COUNT(available.id) AS total
FROM available;
"""
}
PARAMETERS: dict[str, tuple[str, ...]] = {"query": ("q",)}


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
