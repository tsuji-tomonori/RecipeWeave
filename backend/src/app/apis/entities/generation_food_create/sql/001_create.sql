-- 生成の食材入力を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.generation_food AS t (
    id,
    job_id,
    form_id,
    role
)
VALUES (
    %(row_id)s,
    %(job_id)s,
    %(form_id)s,
    %(role)s
)
RETURNING
    t.id,
    t.created_at,
    t.job_id,
    t.form_id,
    t.role,
    t.xmin::TEXT AS etag;
