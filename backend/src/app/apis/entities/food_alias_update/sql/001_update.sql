-- 食材別名を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.food_alias AS t
SET
    food_id = %(food_id)s,
    alias = %(alias)s,
    locale = %(locale)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.food_id,
    t.alias,
    t.locale,
    t.xmin::TEXT AS etag;
