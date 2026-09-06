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
