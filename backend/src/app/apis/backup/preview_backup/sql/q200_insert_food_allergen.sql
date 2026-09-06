-- 検証済みバックアップの食材アレルゲン知識を元IDと全列で復元する。
INSERT INTO recipeweave.food_allergen (
    id,
    created_at,
    form_id,
    allergen_id,
    presence,
    source_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(form_id)s,
    %(allergen_id)s,
    %(presence)s,
    %(source_id)s
);
