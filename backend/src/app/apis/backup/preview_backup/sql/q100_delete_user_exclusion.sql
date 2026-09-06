-- 全置換の確認対象である本人の避けたい食材・物質だけを削除する。
DELETE FROM recipeweave.user_exclusion AS t
WHERE (t.user_id = %(actor_id)s);
