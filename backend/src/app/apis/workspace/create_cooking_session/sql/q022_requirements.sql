-- 工程が占有する器具数と最小容量を読む。
SELECT
    sr.step_id,
    sr.resource_type_id,
    sr.quantity,
    sr.capacity_min,
    rt.name,
    rt.code
FROM recipeweave.step_resource AS sr
INNER JOIN recipeweave.resource_type AS rt ON sr.resource_type_id = rt.id
WHERE
    EXISTS (
        SELECT 1 FROM recipeweave.recipe_step AS st INNER JOIN recipeweave.menu_item AS mi
            ON st.recipe_version_id = mi.recipe_version_id
        WHERE mi.menu_id = %(menu_id)s AND st.id = sr.step_id
    )
ORDER BY sr.step_id, rt.code;
