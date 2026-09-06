-- 動作パラメータ定義を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.operation_parameter AS t
SET
    operation_id = %(operation_id)s,
    code = %(code)s,
    name = %(name)s,
    value_type = %(value_type)s,
    unit_id = %(unit_id)s,
    required = %(required)s,
    min_value = %(min_value)s,
    max_value = %(max_value)s,
    allowed_values = %(allowed_values)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.operation_id,
    t.code,
    t.name,
    t.value_type,
    t.unit_id,
    t.required,
    t.min_value,
    t.max_value,
    t.allowed_values,
    t.xmin::TEXT AS etag;
