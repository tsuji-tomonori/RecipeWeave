-- 市販商品識別を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.food_id,
    t.brand,
    t.name,
    t.gtin,
    t.status,
    t.xmin::TEXT AS etag
FROM recipeweave.product AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
