-- 検証済みバックアップの市販商品識別を元IDと全列で復元する。
INSERT INTO recipeweave.product (
    id,
    created_at,
    food_id,
    brand,
    name,
    gtin,
    status
) VALUES (
    %(id)s,
    %(created_at)s,
    %(food_id)s,
    %(brand)s,
    %(name)s,
    %(gtin)s,
    %(status)s
);
