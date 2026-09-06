-- 形態・商品別栄養値を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.nutrition_fact AS t (
    id,
    form_id,
    product_version_id,
    nutrient_id,
    amount,
    basis_amount,
    basis_unit_id,
    source_id
)
VALUES (
    %(row_id)s,
    %(form_id)s,
    %(product_version_id)s,
    %(nutrient_id)s,
    %(amount)s,
    %(basis_amount)s,
    %(basis_unit_id)s,
    %(source_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.form_id,
    t.product_version_id,
    t.nutrient_id,
    t.amount,
    t.basis_amount,
    t.basis_unit_id,
    t.source_id,
    t.xmin::TEXT AS etag;
