-- ユーザーの嗜好を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.user_id,
    t.option_id,
    t.weight,
    t.xmin::TEXT AS etag
FROM recipeweave.user_preference AS t
WHERE
    t.id = %(row_id)s
    AND t.user_id = %(actor_id)s;
