-- 市販商品識別を一覧取得する。
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
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
