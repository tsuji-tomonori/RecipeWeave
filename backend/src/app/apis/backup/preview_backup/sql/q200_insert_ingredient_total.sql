-- 検証済みバックアップの献立材料集計結果を元IDと全列で復元する。
INSERT INTO recipeweave.ingredient_total (
    id,
    created_at,
    session_id,
    form_id,
    product_version_id,
    unit_id,
    required_amount,
    quality,
    calculation_version,
    actual_amount,
    consumption_outcome
) VALUES (
    %(id)s,
    %(created_at)s,
    %(session_id)s,
    %(form_id)s,
    %(product_version_id)s,
    %(unit_id)s,
    %(required_amount)s,
    %(quality)s,
    %(calculation_version)s,
    %(actual_amount)s,
    %(consumption_outcome)s
);
