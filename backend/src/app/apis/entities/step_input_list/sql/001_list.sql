-- 工程への材料受渡しを一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.step_id,
    t.material_id,
    t.fraction,
    t.xmin::TEXT AS etag
FROM recipeweave.step_input AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
