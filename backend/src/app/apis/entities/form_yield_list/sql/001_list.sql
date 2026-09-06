-- 処理歩留まりを一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.input_form_id,
    t.output_form_id,
    t.yield_ratio,
    t.source_id,
    t.quality,
    t.conditions,
    t.xmin::TEXT AS etag
FROM recipeweave.form_yield AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
