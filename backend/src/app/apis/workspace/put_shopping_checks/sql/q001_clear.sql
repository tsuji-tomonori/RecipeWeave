-- 現在の買い物確認を本人の範囲で置き換える。
DELETE FROM recipeweave.user_shopping_check
WHERE user_id = %(user_id)s;
