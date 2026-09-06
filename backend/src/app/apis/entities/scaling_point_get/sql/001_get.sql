-- 検証済み換算点を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.rule_id,
    t.servings,
    t.multiplier,
    t.xmin::TEXT AS etag
FROM recipeweave.scaling_point AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
