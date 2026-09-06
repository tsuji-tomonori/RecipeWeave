-- レシピ材料明細を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
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
    t.xmin::TEXT AS etag
FROM recipeweave.recipe_ingredient AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
