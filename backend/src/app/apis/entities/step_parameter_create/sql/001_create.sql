-- 工程の型付きパラメータを作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.step_parameter AS t (
    id,
    step_id,
    parameter_id,
    number_value,
    text_value,
    bool_value
)
VALUES (
    %(row_id)s,
    %(step_id)s,
    %(parameter_id)s,
    %(number_value)s,
    %(text_value)s,
    %(bool_value)s
)
RETURNING
    t.id,
    t.created_at,
    t.step_id,
    t.parameter_id,
    t.number_value,
    t.text_value,
    t.bool_value,
    t.xmin::TEXT AS etag;
