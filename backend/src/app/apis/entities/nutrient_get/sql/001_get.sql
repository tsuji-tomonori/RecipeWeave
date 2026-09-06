-- 栄養成分種別を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.unit_label,
    t.xmin::TEXT AS etag
FROM recipeweave.nutrient AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
