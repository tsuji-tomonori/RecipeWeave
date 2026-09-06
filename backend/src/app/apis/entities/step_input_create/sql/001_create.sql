-- 工程への材料受渡しを作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.step_input AS t (
    id,
    step_id,
    material_id,
    fraction
)
VALUES (
    %(row_id)s,
    %(step_id)s,
    %(material_id)s,
    %(fraction)s
)
RETURNING
    t.id,
    t.created_at,
    t.step_id,
    t.material_id,
    t.fraction,
    t.xmin::TEXT AS etag;
