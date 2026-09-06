-- 人数変更規則を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.scaling_rule AS t (
    id,
    name,
    mode,
    min_servings,
    max_servings,
    batch_capacity,
    round_mode,
    round_increment,
    source_id
)
VALUES (
    %(row_id)s,
    %(name)s,
    %(mode)s,
    %(min_servings)s,
    %(max_servings)s,
    %(batch_capacity)s,
    %(round_mode)s,
    %(round_increment)s,
    %(source_id)s
)
RETURNING
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
    t.xmin::TEXT AS etag;
