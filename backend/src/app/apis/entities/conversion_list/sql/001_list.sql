-- 食材形態別換算を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.form_id,
    t.from_unit_id,
    t.to_unit_id,
    t.factor,
    t.quality,
    t.source_id,
    t.conditions,
    t.release_id,
    t.xmin::TEXT AS etag
FROM recipeweave.conversion AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
