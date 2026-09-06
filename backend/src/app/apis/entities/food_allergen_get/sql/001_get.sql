-- 食材アレルゲン知識を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.form_id,
    t.allergen_id,
    t.presence,
    t.source_id,
    t.xmin::TEXT AS etag
FROM recipeweave.food_allergen AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
