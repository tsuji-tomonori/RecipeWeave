-- 検証済みバックアップの処理歩留まりを元IDと全列で復元する。
INSERT INTO recipeweave.form_yield (
    id,
    created_at,
    input_form_id,
    output_form_id,
    yield_ratio,
    source_id,
    quality,
    conditions
) VALUES (
    %(id)s,
    %(created_at)s,
    %(input_form_id)s,
    %(output_form_id)s,
    %(yield_ratio)s,
    %(source_id)s,
    %(quality)s,
    %(conditions)s
);
