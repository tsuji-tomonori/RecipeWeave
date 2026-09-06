-- 試行済み設計点の台帳を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.candidate_attempt AS t (
    id,
    template_id,
    ordinal,
    design_key,
    job_id,
    state,
    reason_code,
    recipe_version_id,
    attempts
)
VALUES (
    %(row_id)s,
    %(template_id)s,
    %(ordinal)s,
    %(design_key)s,
    %(job_id)s,
    %(state)s,
    %(reason_code)s,
    %(recipe_version_id)s,
    %(attempts)s
)
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
