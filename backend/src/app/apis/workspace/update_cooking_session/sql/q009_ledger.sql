-- 同一セッションとロットの二重消費を一意制約で防ぐ。
INSERT INTO recipeweave.pantry_consumption (id, user_id, session_id, lot_id, amount, unit_id)
VALUES (%(row_id)s, %(user_id)s, %(session_id)s, %(lot_id)s, %(amount)s, %(unit_id)s);
