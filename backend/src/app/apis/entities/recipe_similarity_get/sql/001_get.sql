-- 近似レシピ関係を取得する。
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
    t.id = %(row_id)s
    AND TRUE;
