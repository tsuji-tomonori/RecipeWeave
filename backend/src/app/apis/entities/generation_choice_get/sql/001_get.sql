-- 生成軸の選択値を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.job_id,
    t.option_id,
    t.xmin::TEXT AS etag
FROM recipeweave.generation_choice AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
