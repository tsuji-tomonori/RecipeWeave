-- 生成の食材入力を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.job_id,
    t.form_id,
    t.role,
    t.xmin::TEXT AS etag
FROM recipeweave.generation_food AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
