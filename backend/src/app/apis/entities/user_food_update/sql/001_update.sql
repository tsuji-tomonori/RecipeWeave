-- 利用者が追加した独自食材の所有を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.user_food AS t
SET
    user_id = %(user_id)s,
    food_id = %(food_id)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND t.user_id = %(actor_id)s
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.food_id,
    t.xmin::TEXT AS etag;
