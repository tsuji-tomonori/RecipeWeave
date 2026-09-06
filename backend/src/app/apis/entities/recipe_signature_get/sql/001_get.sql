-- 内容重複判定署名を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.algorithm_version,
    t.exact_hash,
    t.canonical_payload,
    t.cluster_key,
    t.xmin::TEXT AS etag
FROM recipeweave.recipe_signature AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
