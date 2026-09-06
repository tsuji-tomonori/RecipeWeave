-- 採用率・飽和度の実測を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.template_id,
    t.window_start,
    t.window_end,
    t.attempted,
    t.valid,
    t.unique_count,
    t.publishable,
    t.input_tokens,
    t.output_tokens,
    t.cost_amount,
    t.currency,
    t.stratum_key,
    t.xmin::TEXT AS etag
FROM recipeweave.generation_stratum_metric AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
