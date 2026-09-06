-- 工程の資源要求を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.step_id,
    t.resource_type_id,
    t.quantity,
    t.capacity_min,
    t.exclusive,
    t.xmin::TEXT AS etag
FROM recipeweave.step_resource AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
