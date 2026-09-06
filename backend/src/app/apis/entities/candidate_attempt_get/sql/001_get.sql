-- 試行済み設計点の台帳を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.template_id,
    t.ordinal,
    t.design_key,
    t.job_id,
    t.state,
    t.reason_code,
    t.recipe_version_id,
    t.attempts,
    t.xmin::TEXT AS etag
FROM recipeweave.candidate_attempt AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
