-- 食材別名を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.food_alias AS t (
    id,
    food_id,
    alias,
    locale
)
VALUES (
    %(row_id)s,
    %(food_id)s,
    %(alias)s,
    %(locale)s
)
RETURNING
    t.id,
    t.created_at,
    t.food_id,
    t.alias,
    t.locale,
    t.xmin::TEXT AS etag;
