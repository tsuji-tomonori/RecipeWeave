-- 生成軸の選択値を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.generation_choice AS t
SET
    job_id = %(job_id)s,
    option_id = %(option_id)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.job_id,
    t.option_id,
    t.xmin::TEXT AS etag;
