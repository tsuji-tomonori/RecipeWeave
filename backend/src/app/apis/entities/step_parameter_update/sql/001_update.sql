-- 工程の型付きパラメータを条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.step_parameter AS t
SET
    step_id = %(step_id)s,
    parameter_id = %(parameter_id)s,
    number_value = %(number_value)s,
    text_value = %(text_value)s,
    bool_value = %(bool_value)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.step_id,
    t.parameter_id,
    t.number_value,
    t.text_value,
    t.bool_value,
    t.xmin::TEXT AS etag;
