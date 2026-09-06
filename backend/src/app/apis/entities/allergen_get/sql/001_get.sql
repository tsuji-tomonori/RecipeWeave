-- アレルゲン概念を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.source_id,
    t.xmin::TEXT AS etag
FROM recipeweave.allergen AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
