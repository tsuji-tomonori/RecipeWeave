-- 指定料理版の安全・材料・品質に基づく先行条件を読む。
SELECT
    %(item_id)s::UUID AS item_id,
    d.before_step_id,
    d.after_step_id,
    d.min_lag_s,
    d.max_lag_s,
    d.kind
FROM recipeweave.recipe_step AS st
INNER JOIN recipeweave.step_dependency AS d ON st.id = d.after_step_id
WHERE st.recipe_version_id = %(version_id)s
ORDER BY d.id;
