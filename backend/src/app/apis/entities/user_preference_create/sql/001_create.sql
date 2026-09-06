-- ユーザーの嗜好を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.user_preference AS t (
    id,
    user_id,
    option_id,
    weight
)
VALUES (
    %(row_id)s,
    %(user_id)s,
    %(option_id)s,
    %(weight)s
)
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.option_id,
    t.weight,
    t.xmin::TEXT AS etag;
