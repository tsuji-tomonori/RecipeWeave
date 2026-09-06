-- 栄養成分種別を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.nutrient AS t
SET
    code = %(code)s,
    name = %(name)s,
    unit_label = %(unit_label)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.unit_label,
    t.xmin::TEXT AS etag;
