-- 人数変更規則を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.name,
    t.mode,
    t.min_servings,
    t.max_servings,
    t.batch_capacity,
    t.round_mode,
    t.round_increment,
    t.source_id,
    t.xmin::TEXT AS etag
FROM recipeweave.scaling_rule AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
