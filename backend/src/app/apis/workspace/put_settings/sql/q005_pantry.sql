-- 常備指定は食品ごとの関連行として保存する。
INSERT INTO recipeweave.user_pantry_food (id, user_id, food_id) VALUES (
    %(row_id)s, %(user_id)s, %(food_id)s
);
