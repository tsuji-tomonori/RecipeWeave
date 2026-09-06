-- 生成結果の出自を取得する。
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
    t.id = %(row_id)s
    AND TRUE;
