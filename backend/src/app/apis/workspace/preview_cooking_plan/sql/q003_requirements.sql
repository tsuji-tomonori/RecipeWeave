-- 工程が必要とする器具の台数と単位容量を読む。
SELECT
    sr.step_id,
    sr.resource_type_id,
    sr.quantity,
    sr.capacity_min,
    sr.exclusive,
    rt.name,
    rt.code
FROM recipeweave.step_resource AS sr
INNER JOIN recipeweave.recipe_step AS st ON sr.step_id = st.id
INNER JOIN recipeweave.resource_type AS rt ON sr.resource_type_id = rt.id
WHERE st.recipe_version_id = %(version_id)s
ORDER BY sr.step_id, rt.code;
