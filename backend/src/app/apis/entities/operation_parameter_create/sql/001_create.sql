-- 動作パラメータ定義を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.operation_parameter AS t (
    id,
    operation_id,
    code,
    name,
    value_type,
    unit_id,
    required,
    min_value,
    max_value,
    allowed_values
)
VALUES (
    %(row_id)s,
    %(operation_id)s,
    %(code)s,
    %(name)s,
    %(value_type)s,
    %(unit_id)s,
    %(required)s,
    %(min_value)s,
    %(max_value)s,
    %(allowed_values)s
)
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
