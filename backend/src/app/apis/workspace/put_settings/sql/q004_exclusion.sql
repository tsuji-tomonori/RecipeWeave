-- 除外する食品を明示して保存する。
INSERT INTO recipeweave.user_exclusion (id, user_id, food_id, allergen_id, strict)
VALUES (%(row_id)s, %(user_id)s, %(food_id)s, NULL, TRUE);
