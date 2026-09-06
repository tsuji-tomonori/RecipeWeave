-- 利用者が追加した独自食材の所有を条件付き削除する。
-- 値は名前付きパラメータで束縛する。
DELETE FROM recipeweave.user_food AS t
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
