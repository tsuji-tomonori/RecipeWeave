-- 在庫の減算と台帳の追記は同じ要求トランザクションで確定する。
UPDATE recipeweave.pantry_lot SET amount = amount - %(amount)s, updated_at = CURRENT_TIMESTAMP
WHERE id = %(lot_id)s AND user_id = %(user_id)s AND amount >= %(amount)s RETURNING id;
