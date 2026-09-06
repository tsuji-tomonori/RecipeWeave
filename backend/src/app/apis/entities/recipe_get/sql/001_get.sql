-- レシピ同一性を取得する。
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
    t.id = %(row_id)s
    AND TRUE;
