-- 試行済み設計点の台帳を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.candidate_attempt AS t
SET
    template_id = %(template_id)s,
    ordinal = %(ordinal)s,
    design_key = %(design_key)s,
    job_id = %(job_id)s,
    state = %(state)s,
    reason_code = %(reason_code)s,
    recipe_version_id = %(recipe_version_id)s,
    attempts = %(attempts)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
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
    t.xmin::TEXT AS etag;
