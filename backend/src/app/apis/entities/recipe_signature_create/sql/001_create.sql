-- 内容重複判定署名を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.recipe_signature AS t (
    id,
    recipe_version_id,
    algorithm_version,
    exact_hash,
    canonical_payload,
    cluster_key
)
VALUES (
    %(row_id)s,
    %(recipe_version_id)s,
    %(algorithm_version)s,
    %(exact_hash)s,
    %(canonical_payload)s,
    %(cluster_key)s
)
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.algorithm_version,
    t.exact_hash,
    t.canonical_payload,
    t.cluster_key,
    t.xmin::TEXT AS etag;
