-- 食材の分類属性を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.food_axis_option AS t
SET
    food_id = %(food_id)s,
    option_id = %(option_id)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.food_id,
    t.option_id,
    t.xmin::TEXT AS etag;
