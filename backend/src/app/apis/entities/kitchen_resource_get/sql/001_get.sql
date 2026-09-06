-- キッチンの実資源を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.user_id,
    t.resource_type_id,
    t.name,
    t.capacity,
    t.quantity,
    t.active,
    t.xmin::TEXT AS etag
FROM recipeweave.kitchen_resource AS t
WHERE
    t.id = %(row_id)s
    AND t.user_id = %(actor_id)s;
