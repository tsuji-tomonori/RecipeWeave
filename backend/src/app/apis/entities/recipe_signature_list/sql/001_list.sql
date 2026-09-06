-- 内容重複判定署名を一覧取得する。
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
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
