-- レシピ同一性を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.recipe AS t
SET
    title = %(title)s,
    family_option_id = %(family_option_id)s,
    status = %(status)s,
    withdrawal_reason = %(withdrawal_reason)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.title,
    t.family_option_id,
    t.status,
    t.withdrawal_reason,
    t.xmin::TEXT AS etag;
