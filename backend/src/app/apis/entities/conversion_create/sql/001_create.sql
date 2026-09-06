-- 食材形態別換算を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.conversion AS t (
    id,
    form_id,
    from_unit_id,
    to_unit_id,
    factor,
    quality,
    source_id,
    conditions,
    release_id
)
VALUES (
    %(row_id)s,
    %(form_id)s,
    %(from_unit_id)s,
    %(to_unit_id)s,
    %(factor)s,
    %(quality)s,
    %(source_id)s,
    %(conditions)s,
    %(release_id)s
)
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
