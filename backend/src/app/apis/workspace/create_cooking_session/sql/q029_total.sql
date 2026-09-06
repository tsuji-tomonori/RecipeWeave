-- 同じ商品・形態・単位の確定需要を一つに合計する。
INSERT INTO recipeweave.ingredient_total
(
    id,
    session_id,
    form_id,
    product_version_id,
    unit_id,
    required_amount,
    quality,
    calculation_version
)
VALUES (
    %(row_id)s,
    %(session_id)s,
    %(form_id)s,
    %(product_id)s,
    %(unit_id)s,
    %(amount)s,
    'reference',
    'decimal-v1'
);
