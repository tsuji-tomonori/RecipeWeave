-- 同一料理版の材料・品質・安全上の先行条件を読む。
SELECT
    mi.id AS item_id,
    d.before_step_id,
    d.after_step_id,
    d.min_lag_s,
    d.max_lag_s,
    d.kind
FROM recipeweave.menu_item AS mi
INNER JOIN recipeweave.recipe_step AS st ON mi.recipe_version_id = st.recipe_version_id
INNER JOIN recipeweave.step_dependency AS d ON st.id = d.after_step_id
WHERE mi.menu_id = %(menu_id)s
ORDER BY mi.position, d.id;
