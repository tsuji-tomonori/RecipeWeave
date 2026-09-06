-- 生成結果の出自を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.job_id,
    t.policy_id,
    t.input_snapshot,
    t.raw_output_uri,
    t.raw_output_hash,
    t.xmin::TEXT AS etag
FROM recipeweave.generation_result AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
