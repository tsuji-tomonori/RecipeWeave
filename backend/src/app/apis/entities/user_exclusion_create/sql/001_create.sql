-- 避けたい食材・物質を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.user_exclusion AS t (
    id,
    user_id,
    food_id,
    allergen_id,
    strict
)
VALUES (
    %(row_id)s,
    %(user_id)s,
    %(food_id)s,
    %(allergen_id)s,
    %(strict)s
)
RETURNING
    t.id,
    t.created_at,
    t.user_id,
    t.food_id,
    t.allergen_id,
    t.strict,
    t.xmin::TEXT AS etag;
