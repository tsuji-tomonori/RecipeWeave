-- 料理版の工程と加熱時間の換算規則を読む。
SELECT
    mi.id AS item_id,
    mi.position,
    mi.servings,
    rv.base_servings,
    rv.recipe_id,
    st.id AS step_id,
    st.step_no,
    st.duration_max_s,
    st.attention,
    sc.mode AS scaling_mode,
    sc.batch_capacity,
    GREATEST(sc.min_servings, (
        SELECT MAX(ingredient_rule.min_servings)
        FROM recipeweave.recipe_ingredient AS ingredient
        INNER JOIN recipeweave.scaling_rule AS ingredient_rule
            ON ingredient.scaling_rule_id = ingredient_rule.id
        WHERE ingredient.recipe_version_id = rv.id
    )) AS min_servings,
    LEAST(sc.max_servings, (
        SELECT MIN(ingredient_rule.max_servings)
        FROM recipeweave.recipe_ingredient AS ingredient
        INNER JOIN recipeweave.scaling_rule AS ingredient_rule
            ON ingredient.scaling_rule_id = ingredient_rule.id
        WHERE ingredient.recipe_version_id = rv.id
    )) AS max_servings
FROM recipeweave.menu_item AS mi
INNER JOIN recipeweave.recipe_version AS rv ON mi.recipe_version_id = rv.id
INNER JOIN recipeweave.recipe_step AS st ON rv.id = st.recipe_version_id
INNER JOIN recipeweave.scaling_rule AS sc ON st.scaling_rule_id = sc.id
WHERE mi.menu_id = %(menu_id)s
ORDER BY mi.position, st.step_no;
