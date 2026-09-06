-- 検証済みバックアップの商品表示アレルゲンを元IDと全列で復元する。
INSERT INTO recipeweave.product_allergen (
    id,
    created_at,
    product_version_id,
    allergen_id,
    presence,
    source_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(product_version_id)s,
    %(allergen_id)s,
    %(presence)s,
    %(source_id)s
);
