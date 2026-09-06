-- 全置換の確認対象である本人の献立だけを削除する。
DELETE FROM recipeweave.menu AS t
WHERE (t.user_id = %(actor_id)s);
