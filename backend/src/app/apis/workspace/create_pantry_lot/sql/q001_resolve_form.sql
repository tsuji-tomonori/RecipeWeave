-- 食材形態と単位をDBから検証し、他人の独自食材は参照させない。
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
