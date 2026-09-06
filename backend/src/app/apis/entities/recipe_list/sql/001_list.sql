-- レシピ同一性を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.title,
    t.family_option_id,
    t.status,
    t.withdrawal_reason,
    t.xmin::TEXT AS etag
FROM recipeweave.recipe AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
