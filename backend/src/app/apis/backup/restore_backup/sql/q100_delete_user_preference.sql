-- 全置換の確認対象である本人のユーザーの嗜好だけを削除する。
DELETE FROM recipeweave.user_preference AS t
WHERE (t.user_id = %(actor_id)s);
