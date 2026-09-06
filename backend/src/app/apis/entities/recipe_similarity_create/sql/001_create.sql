-- 近似レシピ関係を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.recipe_similarity AS t (
    id,
    left_version_id,
    right_version_id,
    algorithm_version,
    score,
    explanation
)
VALUES (
    %(row_id)s,
    %(left_version_id)s,
    %(right_version_id)s,
    %(algorithm_version)s,
    %(score)s,
    %(explanation)s
)
RETURNING
    t.id,
    t.created_at,
    t.left_version_id,
    t.right_version_id,
    t.algorithm_version,
    t.score,
    t.explanation,
    t.xmin::TEXT AS etag;
