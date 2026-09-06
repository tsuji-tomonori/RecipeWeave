-- 市販商品識別を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.product AS t (
    id,
    food_id,
    brand,
    name,
    gtin,
    status
)
VALUES (
    %(row_id)s,
    %(food_id)s,
    %(brand)s,
    %(name)s,
    %(gtin)s,
    %(status)s
)
RETURNING
    t.id,
    t.created_at,
    t.food_id,
    t.brand,
    t.name,
    t.gtin,
    t.status,
    t.xmin::TEXT AS etag;
