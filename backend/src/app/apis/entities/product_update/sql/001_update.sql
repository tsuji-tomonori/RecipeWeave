-- 市販商品識別を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.product AS t
SET
    food_id = %(food_id)s,
    brand = %(brand)s,
    name = %(name)s,
    gtin = %(gtin)s,
    status = %(status)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.food_id,
    t.brand,
    t.name,
    t.gtin,
    t.status,
    t.xmin::TEXT AS etag;
