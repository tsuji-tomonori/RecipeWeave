-- 購買食品から同一性への対応を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.food_id,
    t.identity_id,
    t.normalizer_version,
    t.reason,
    t.xmin::TEXT AS etag
FROM recipeweave.food_identity_member AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
