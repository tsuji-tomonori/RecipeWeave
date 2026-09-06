-- 近似検索用特徴量を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.recipe_embedding AS t (
    id,
    recipe_version_id,
    model_version,
    content_hash,
    embedding,
    created_for_index
)
VALUES (
    %(row_id)s,
    %(recipe_version_id)s,
    %(model_version)s,
    %(content_hash)s,
    %(embedding)s::VECTOR,
    %(created_for_index)s
)
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.model_version,
    t.content_hash,
    t.embedding,
    t.created_for_index,
    t.xmin::TEXT AS etag;
