-- 食材アレルゲン知識を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.food_allergen AS t (
    id,
    form_id,
    allergen_id,
    presence,
    source_id
)
VALUES (
    %(row_id)s,
    %(form_id)s,
    %(allergen_id)s,
    %(presence)s,
    %(source_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.form_id,
    t.allergen_id,
    t.presence,
    t.source_id,
    t.xmin::TEXT AS etag;
