-- 商品仕様版を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.product_id,
    t.version,
    t.form_id,
    t.net_amount,
    t.unit_id,
    t.drain_amount,
    t.source_id,
    t.preparation_note,
    t.valid_from,
    t.xmin::TEXT AS etag
FROM recipeweave.product_version AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
