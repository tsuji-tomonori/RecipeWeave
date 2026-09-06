-- 生成の食材入力を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.generation_food AS t
SET
    job_id = %(job_id)s,
    form_id = %(form_id)s,
    role = %(role)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.job_id,
    t.form_id,
    t.role,
    t.xmin::TEXT AS etag;
