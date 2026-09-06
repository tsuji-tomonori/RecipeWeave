-- 採用率・飽和度の実測を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.generation_stratum_metric AS t (
    id,
    template_id,
    window_start,
    window_end,
    attempted,
    valid,
    unique_count,
    publishable,
    input_tokens,
    output_tokens,
    cost_amount,
    currency,
    stratum_key
)
VALUES (
    %(row_id)s,
    %(template_id)s,
    %(window_start)s,
    %(window_end)s,
    %(attempted)s,
    %(valid)s,
    %(unique_count)s,
    %(publishable)s,
    %(input_tokens)s,
    %(output_tokens)s,
    %(cost_amount)s,
    %(currency)s,
    %(stratum_key)s
)
RETURNING
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
    t.xmin::TEXT AS etag;
