-- 食材形態別換算を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.conversion AS t
SET
    form_id = %(form_id)s,
    from_unit_id = %(from_unit_id)s,
    to_unit_id = %(to_unit_id)s,
    factor = %(factor)s,
    quality = %(quality)s,
    source_id = %(source_id)s,
    conditions = %(conditions)s,
    release_id = %(release_id)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.form_id,
    t.from_unit_id,
    t.to_unit_id,
    t.factor,
    t.quality,
    t.source_id,
    t.conditions,
    t.release_id,
    t.xmin::TEXT AS etag;
