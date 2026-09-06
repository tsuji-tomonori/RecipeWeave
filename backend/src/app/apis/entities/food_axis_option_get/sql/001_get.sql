-- 食材の分類属性を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.food_id,
    t.option_id,
    t.xmin::TEXT AS etag
FROM recipeweave.food_axis_option AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
