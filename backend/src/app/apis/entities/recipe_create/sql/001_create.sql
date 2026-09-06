-- レシピ同一性を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.recipe AS t (
    id,
    title,
    family_option_id,
    status,
    withdrawal_reason
)
VALUES (
    %(row_id)s,
    %(title)s,
    %(family_option_id)s,
    %(status)s,
    %(withdrawal_reason)s
)
RETURNING
    t.id,
    t.created_at,
    t.title,
    t.family_option_id,
    t.status,
    t.withdrawal_reason,
    t.xmin::TEXT AS etag;
