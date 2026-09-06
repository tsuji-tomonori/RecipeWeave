-- レシピ内容版を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.recipe_version AS t
SET
    recipe_id = %(recipe_id)s,
    version = %(version)s,
    release_id = %(release_id)s,
    base_servings = %(base_servings)s,
    output_amount = %(output_amount)s,
    output_unit_id = %(output_unit_id)s,
    status = %(status)s,
    validation = %(validation)s,
    content_hash = %(content_hash)s,
    published_at = %(published_at)s,
    description = %(description)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
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
