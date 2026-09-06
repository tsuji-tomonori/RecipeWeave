-- 近似検索用特徴量を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.model_version,
    t.content_hash,
    t.embedding,
    t.created_for_index,
    t.xmin::TEXT AS etag
FROM recipeweave.recipe_embedding AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
