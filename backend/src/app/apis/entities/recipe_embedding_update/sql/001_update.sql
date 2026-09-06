-- 近似検索用特徴量を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.recipe_embedding AS t
SET
    recipe_version_id = %(recipe_version_id)s,
    model_version = %(model_version)s,
    content_hash = %(content_hash)s,
    embedding = %(embedding)s::VECTOR,
    created_for_index = %(created_for_index)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.model_version,
    t.content_hash,
    t.embedding,
    t.created_for_index,
    t.xmin::TEXT AS etag;
