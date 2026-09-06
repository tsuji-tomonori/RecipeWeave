-- 本人の設定だけを、同じトランザクション内で置き換える。
DELETE FROM recipeweave.user_exclusion
WHERE user_id = %(user_id)s;
