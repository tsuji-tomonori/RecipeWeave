-- 形態・商品別栄養値を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.form_id,
    t.product_version_id,
    t.nutrient_id,
    t.amount,
    t.basis_amount,
    t.basis_unit_id,
    t.source_id,
    t.xmin::TEXT AS etag
FROM recipeweave.nutrition_fact AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
