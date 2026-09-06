-- 工程の資源要求を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.step_resource AS t
SET
    step_id = %(step_id)s,
    resource_type_id = %(resource_type_id)s,
    quantity = %(quantity)s,
    capacity_min = %(capacity_min)s,
    exclusive = %(exclusive)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.step_id,
    t.resource_type_id,
    t.quantity,
    t.capacity_min,
    t.exclusive,
    t.xmin::TEXT AS etag;
