-- 食材の分類属性を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.food_axis_option AS t (
    id,
    food_id,
    option_id
)
VALUES (
    %(row_id)s,
    %(food_id)s,
    %(option_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.food_id,
    t.option_id,
    t.xmin::TEXT AS etag;
