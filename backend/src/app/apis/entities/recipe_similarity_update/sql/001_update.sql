-- 近似レシピ関係を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.recipe_similarity AS t
SET
    left_version_id = %(left_version_id)s,
    right_version_id = %(right_version_id)s,
    algorithm_version = %(algorithm_version)s,
    score = %(score)s,
    explanation = %(explanation)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.left_version_id,
    t.right_version_id,
    t.algorithm_version,
    t.score,
    t.explanation,
    t.xmin::TEXT AS etag;
