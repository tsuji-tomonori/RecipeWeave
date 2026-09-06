-- 検証済みバックアップのキッチンの実資源を元IDと全列で復元する。
INSERT INTO recipeweave.kitchen_resource (
    id,
    created_at,
    user_id,
    resource_type_id,
    name,
    capacity,
    quantity,
    active
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(resource_type_id)s,
    %(name)s,
    %(capacity)s,
    %(quantity)s,
    %(active)s
);
