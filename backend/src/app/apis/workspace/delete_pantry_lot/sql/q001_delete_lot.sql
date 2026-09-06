-- 履歴と消費台帳の参照を保ったまま本人の在庫を無効化する。
UPDATE recipeweave.pantry_lot SET status = 'deleted', updated_at = CURRENT_TIMESTAMP
WHERE id = %(row_id)s AND user_id = %(user_id)s AND status = 'active' RETURNING id;
