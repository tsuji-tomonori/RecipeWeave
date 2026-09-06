-- 全置換の確認対象である本人の調理による在庫消費の冪等台帳だけを削除する。
DELETE FROM recipeweave.pantry_consumption AS t
WHERE (t.user_id = %(actor_id)s);
