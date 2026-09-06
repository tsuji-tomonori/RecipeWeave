-- 栄養成分種別を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.nutrient AS t (
    id,
    code,
    name,
    unit_label
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(name)s,
    %(unit_label)s
)
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.unit_label,
    t.xmin::TEXT AS etag;
