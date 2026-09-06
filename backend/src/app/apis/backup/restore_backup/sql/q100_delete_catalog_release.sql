-- 全置換の確認対象である本人のカタログ公開版だけを削除する。
DELETE FROM recipeweave.catalog_release AS t
WHERE (t.owner_id = %(actor_id)s);
