-- 検証済みバックアップのセット内構成品を元IDと全列で復元する。
INSERT INTO recipeweave.product_component (
    id,
    created_at,
    product_version_id,
    form_id,
    name,
    amount,
    unit_id,
    quality
) VALUES (
    %(id)s,
    %(created_at)s,
    %(product_version_id)s,
    %(form_id)s,
    %(name)s,
    %(amount)s,
    %(unit_id)s,
    %(quality)s
);
