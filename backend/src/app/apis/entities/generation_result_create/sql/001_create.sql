-- 生成結果の出自を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.generation_result AS t (
    id,
    recipe_version_id,
    job_id,
    policy_id,
    input_snapshot,
    raw_output_uri,
    raw_output_hash
)
VALUES (
    %(row_id)s,
    %(recipe_version_id)s,
    %(job_id)s,
    %(policy_id)s,
    %(input_snapshot)s,
    %(raw_output_uri)s,
    %(raw_output_hash)s
)
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.job_id,
    t.policy_id,
    t.input_snapshot,
    t.raw_output_uri,
    t.raw_output_hash,
    t.xmin::TEXT AS etag;
