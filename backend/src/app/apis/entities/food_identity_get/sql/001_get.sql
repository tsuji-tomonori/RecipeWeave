-- 料理同一性上の食品を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.normalizer_version,
    t.xmin::TEXT AS etag
FROM recipeweave.food_identity AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
