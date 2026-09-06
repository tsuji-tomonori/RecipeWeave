-- 独自食材の所有者を認証主体へ固定する。
INSERT INTO recipeweave.user_food (id, user_id, food_id) VALUES (
    %(row_id)s, %(user_id)s, %(food_id)s
);
