-- 検証済みバックアップの形態・商品別栄養値を元IDと全列で復元する。
INSERT INTO recipeweave.nutrition_fact (
    id,
    created_at,
    form_id,
    product_version_id,
    nutrient_id,
    amount,
    basis_amount,
    basis_unit_id,
    source_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(form_id)s,
    %(product_version_id)s,
    %(nutrient_id)s,
    %(amount)s,
    %(basis_amount)s,
    %(basis_unit_id)s,
    %(source_id)s
);
