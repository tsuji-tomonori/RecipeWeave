-- 工程への材料受渡しを取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.step_id,
    t.material_id,
    t.fraction,
    t.xmin::TEXT AS etag
FROM recipeweave.step_input AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
