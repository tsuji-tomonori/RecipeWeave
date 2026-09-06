-- 動作パラメータ定義を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
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
    t.xmin::TEXT AS etag
FROM recipeweave.operation_parameter AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
