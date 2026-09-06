-- 調理計画が参照する献立版を更新する。
UPDATE recipeweave.menu SET revision = revision + 1
WHERE id = %(menu_id)s AND user_id = %(user_id)s RETURNING revision;
