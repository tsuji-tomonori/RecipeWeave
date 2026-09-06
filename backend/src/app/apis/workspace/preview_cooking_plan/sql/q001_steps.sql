-- 指定料理版の工程を要求の献立行IDへ対応させる。永続行は作成しない。
SELECT
    %(item_id)s::UUID AS item_id,
    %(position)s::INTEGER AS position,
    %(servings)s::NUMERIC AS servings,
    rv.base_servings,
    rv.recipe_id,
    st.id AS step_id,
    st.step_no,
    st.duration_max_s,
    st.attention,
    sc.mode AS scaling_mode,
    sc.batch_capacity,
    sc.min_servings,
    sc.max_servings
FROM recipeweave.recipe_version AS rv
INNER JOIN recipeweave.recipe_step AS st ON rv.id = st.recipe_version_id
INNER JOIN recipeweave.scaling_rule AS sc ON st.scaling_rule_id = sc.id
WHERE rv.id = %(version_id)s
ORDER BY st.step_no;
