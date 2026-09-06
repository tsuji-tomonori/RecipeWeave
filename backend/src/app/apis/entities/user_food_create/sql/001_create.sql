-- 利用者が追加した独自食材の所有を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.user_food AS t (
    id,
    user_id,
    food_id
)
VALUES (
    %(row_id)s,
    %(user_id)s,
    %(food_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.food_id,
    t.xmin::TEXT AS etag;
