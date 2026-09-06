-- 商品固有の調理条件を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.product_version_id,
    t.operation_id,
    t.allowed,
    t.use_original_container,
    t.parameter_contract,
    t.source_id,
    t.xmin::TEXT AS etag
FROM recipeweave.product_preparation_rule AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
