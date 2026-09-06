-- ユーザーの嗜好を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.user_preference AS t
SET
    user_id = %(user_id)s,
    option_id = %(option_id)s,
    weight = %(weight)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND t.user_id = %(actor_id)s
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.option_id,
    t.weight,
    t.xmin::TEXT AS etag;
