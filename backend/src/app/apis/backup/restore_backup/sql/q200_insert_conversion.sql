-- 検証済みバックアップの食材形態別換算を元IDと全列で復元する。
INSERT INTO recipeweave.conversion (
    id,
    created_at,
    form_id,
    from_unit_id,
    to_unit_id,
    factor,
    quality,
    source_id,
    conditions,
    release_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(form_id)s,
    %(from_unit_id)s,
    %(to_unit_id)s,
    %(factor)s,
    %(quality)s,
    %(source_id)s,
    %(conditions)s,
    %(release_id)s
);
