-- キッチンの実資源を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.kitchen_resource AS t (
    id,
    user_id,
    resource_type_id,
    name,
    capacity,
    quantity,
    active
)
VALUES (
    %(row_id)s,
    %(user_id)s,
    %(resource_type_id)s,
    %(name)s,
    %(capacity)s,
    %(quantity)s,
    %(active)s
)
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.resource_type_id,
    t.name,
    t.capacity,
    t.quantity,
    t.active,
    t.xmin::TEXT AS etag;
