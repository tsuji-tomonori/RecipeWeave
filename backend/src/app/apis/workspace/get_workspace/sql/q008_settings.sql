-- 除外・常備・器具を各設定表から一覧化する。
SELECT
    'excluded' AS kind,
    food_id::TEXT AS value
FROM recipeweave.user_exclusion
WHERE user_id = %(user_id)s AND food_id IS NOT NULL
UNION ALL
SELECT
    'pantry',
    food_id::TEXT
FROM recipeweave.user_pantry_food
WHERE user_id = %(user_id)s
UNION ALL
SELECT
    'equipment',
    r.name
FROM recipeweave.kitchen_resource AS k
INNER JOIN recipeweave.resource_type AS r ON k.resource_type_id = r.id
WHERE k.user_id = %(user_id)s AND k.active AND r.code NOT IN ('person', 'burner', 'bowl');
