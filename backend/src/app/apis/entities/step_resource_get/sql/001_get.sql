-- 工程の資源要求を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.step_id,
    t.resource_type_id,
    t.quantity,
    t.capacity_min,
    t.exclusive,
    t.xmin::TEXT AS etag
FROM recipeweave.step_resource AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
