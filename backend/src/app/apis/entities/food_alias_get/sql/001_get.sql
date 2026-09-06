-- 食材別名を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.food_id,
    t.alias,
    t.locale,
    t.xmin::TEXT AS etag
FROM recipeweave.food_alias AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
