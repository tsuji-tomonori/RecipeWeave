-- 全置換の確認対象である本人の手持ち食材ロットだけを削除する。
DELETE FROM recipeweave.pantry_lot AS t
WHERE (t.user_id = %(actor_id)s);
