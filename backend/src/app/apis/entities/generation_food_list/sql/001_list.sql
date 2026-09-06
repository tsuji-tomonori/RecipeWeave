-- 生成の食材入力を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.job_id,
    t.form_id,
    t.role,
    t.xmin::TEXT AS etag
FROM recipeweave.generation_food AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
