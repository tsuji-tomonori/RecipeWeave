-- レシピ内容版を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.recipe_version AS t (
    id,
    recipe_id,
    version,
    release_id,
    base_servings,
    output_amount,
    output_unit_id,
    status,
    validation,
    content_hash,
    published_at,
    description
)
VALUES (
    %(row_id)s,
    %(recipe_id)s,
    %(version)s,
    %(release_id)s,
    %(base_servings)s,
    %(output_amount)s,
    %(output_unit_id)s,
    %(status)s,
    %(validation)s,
    %(content_hash)s,
    %(published_at)s,
    %(description)s
)
RETURNING
    t.id,
    t.created_at,
    t.recipe_id,
    t.version,
    t.release_id,
    t.base_servings,
    t.output_amount,
    t.output_unit_id,
    t.status,
    t.validation,
    t.content_hash,
    t.published_at,
    t.description,
    t.xmin::TEXT AS etag;
