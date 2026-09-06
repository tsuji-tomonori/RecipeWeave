-- 近似レシピ関係を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.left_version_id,
    t.right_version_id,
    t.algorithm_version,
    t.score,
    t.explanation,
    t.xmin::TEXT AS etag
FROM recipeweave.recipe_similarity AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
