-- 避けたい食材・物質を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.user_id,
    t.food_id,
    t.allergen_id,
    t.strict,
    t.xmin::TEXT AS etag
FROM recipeweave.user_exclusion AS t
WHERE
    t.user_id = %(actor_id)s
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
