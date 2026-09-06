-- 人数変更規則を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.name,
    t.mode,
    t.min_servings,
    t.max_servings,
    t.batch_capacity,
    t.round_mode,
    t.round_increment,
    t.source_id,
    t.xmin::TEXT AS etag
FROM recipeweave.scaling_rule AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
