-- 生成軸の選択値を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.job_id,
    t.option_id,
    t.xmin::TEXT AS etag
FROM recipeweave.generation_choice AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
