-- レシピ材料明細を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.recipe_ingredient AS t
SET
    recipe_version_id = %(recipe_version_id)s,
    line_no = %(line_no)s,
    form_id = %(form_id)s,
    product_version_id = %(product_version_id)s,
    component_id = %(component_id)s,
    kit_parent_line_id = %(kit_parent_line_id)s,
    role = %(role)s,
    demand_kind = %(demand_kind)s,
    amount_mode = %(amount_mode)s,
    amount = %(amount)s,
    amount_max = %(amount_max)s,
    unit_id = %(unit_id)s,
    canonical_amount = %(canonical_amount)s,
    conversion_id = %(conversion_id)s,
    scaling_rule_id = %(scaling_rule_id)s,
    optional = %(optional)s,
    note = %(note)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.line_no,
    t.form_id,
    t.product_version_id,
    t.component_id,
    t.kit_parent_line_id,
    t.role,
    t.demand_kind,
    t.amount_mode,
    t.amount,
    t.amount_max,
    t.unit_id,
    t.canonical_amount,
    t.conversion_id,
    t.scaling_rule_id,
    t.optional,
    t.note,
    t.xmin::TEXT AS etag;
