-- 工程の資源要求を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.step_resource AS t (
    id,
    step_id,
    resource_type_id,
    quantity,
    capacity_min,
    exclusive
)
VALUES (
    %(row_id)s,
    %(step_id)s,
    %(resource_type_id)s,
    %(quantity)s,
    %(capacity_min)s,
    %(exclusive)s
)
RETURNING
    t.id,
    t.created_at,
    t.step_id,
    t.resource_type_id,
    t.quantity,
    t.capacity_min,
    t.exclusive,
    t.xmin::TEXT AS etag;
