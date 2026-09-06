-- 既存器具のID・容量・予約を保持して再有効化する。
UPDATE recipeweave.kitchen_resource AS kitchen
SET active = TRUE
FROM recipeweave.resource_type AS resource_kind
WHERE
    kitchen.user_id = %(user_id)s
    AND kitchen.resource_type_id = resource_kind.id
    AND resource_kind.name = %(name)s AND resource_kind.status = 'active'
RETURNING kitchen.id;
