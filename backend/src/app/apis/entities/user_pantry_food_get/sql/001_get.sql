-- 利用者が常備すると設定した食材を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.user_id,
    t.food_id,
    t.xmin::TEXT AS etag
FROM recipeweave.user_pantry_food AS t
WHERE
    t.id = %(row_id)s
    AND t.user_id = %(actor_id)s;
