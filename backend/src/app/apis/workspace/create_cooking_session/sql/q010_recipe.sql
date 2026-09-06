-- 公開済み料理、または明示したローカル試用で利用できる料理版を選ぶ。
SELECT
    rv.id,
    rv.base_servings,
    ARRAY(
        SELECT ao.id FROM recipeweave.recipe_option AS ro
        INNER JOIN recipeweave.axis_option AS ao ON ro.option_id = ao.id
        INNER JOIN recipeweave.axis AS ax ON ao.axis_id = ax.id
        WHERE ro.recipe_version_id = rv.id AND ax.code = 'dish_role'
        ORDER BY ao.id
    ) AS role_option_ids
FROM recipeweave.recipe_version AS rv
INNER JOIN
    recipeweave.recipe AS r
    ON rv.recipe_id = r.id
WHERE
    r.id = %(recipe_id)s
    AND (%(requested_version_id)s::UUID IS NULL OR rv.id = %(requested_version_id)s)
    AND (
        (rv.status = 'published' AND rv.validation = 'passed' AND r.status = 'published')
        OR (%(preview)s AND rv.status = 'draft' AND r.status = 'draft')
    )
ORDER BY rv.version DESC
LIMIT 1;
