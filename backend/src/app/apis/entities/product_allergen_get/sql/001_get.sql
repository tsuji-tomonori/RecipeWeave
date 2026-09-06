-- 商品表示アレルゲンを取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.product_version_id,
    t.allergen_id,
    t.presence,
    t.source_id,
    t.xmin::TEXT AS etag
FROM recipeweave.product_allergen AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
