-- 本人の設定だけを、同じトランザクション内で置き換える。
DELETE FROM recipeweave.user_pantry_food
WHERE user_id = %(user_id)s;
