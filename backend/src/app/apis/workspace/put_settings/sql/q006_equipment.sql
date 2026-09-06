-- 同じ器具の既存ID・容量を維持して再有効化し、未登録時だけ追加する。
WITH enabled AS (
UPDATE recipeweave.kitchen_resource AS k SET active = TRUE
FROM recipeweave.resource_type AS r WHERE k.user_id = %(user_id)s
AND k.resource_type_id = r.id AND r.name = %(name)s AND r.status = 'active' RETURNING k.id
), inserted AS (
INSERT INTO recipeweave.kitchen_resource (id, user_id, resource_type_id, name, capacity, quantity, active)
SELECT %(row_id)s, %(user_id)s, r.id, r.name, NULL, 1, TRUE FROM recipeweave.resource_type AS r
WHERE r.name = %(name)s AND r.status = 'active' AND NOT EXISTS (SELECT 1 FROM enabled) RETURNING id
) SELECT id FROM enabled UNION ALL SELECT id FROM inserted;
