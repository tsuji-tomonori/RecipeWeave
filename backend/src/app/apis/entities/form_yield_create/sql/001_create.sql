-- 処理歩留まりを作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.form_yield AS t (
    id,
    input_form_id,
    output_form_id,
    yield_ratio,
    source_id,
    quality,
    conditions
)
VALUES (
    %(row_id)s,
    %(input_form_id)s,
    %(output_form_id)s,
    %(yield_ratio)s,
    %(source_id)s,
    %(quality)s,
    %(conditions)s
)
RETURNING
    t.id,
    t.created_at,
    t.input_form_id,
    t.output_form_id,
    t.yield_ratio,
    t.source_id,
    t.quality,
    t.conditions,
    t.xmin::TEXT AS etag;
