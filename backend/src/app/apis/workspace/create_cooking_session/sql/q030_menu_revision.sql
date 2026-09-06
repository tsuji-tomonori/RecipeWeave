-- 計画が参照する専用献立の確定版を読む。
SELECT revision FROM recipeweave.menu
WHERE id = %(menu_id)s AND user_id = %(user_id)s;
