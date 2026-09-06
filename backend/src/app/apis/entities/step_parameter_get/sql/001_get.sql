-- 工程の型付きパラメータを取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.step_id,
    t.parameter_id,
    t.number_value,
    t.text_value,
    t.bool_value,
    t.xmin::TEXT AS etag
FROM recipeweave.step_parameter AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
