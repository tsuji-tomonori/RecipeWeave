-- 工程への材料受渡しを条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.step_input AS t
SET
    step_id = %(step_id)s,
    material_id = %(material_id)s,
    fraction = %(fraction)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.step_id,
    t.material_id,
    t.fraction,
    t.xmin::TEXT AS etag;
