-- 組み合わせ・公開ルールを一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.code,
    t.version,
    t.severity,
    t.predicate,
    t.message,
    t.source_id,
    t.status,
    t.xmin::TEXT AS etag
FROM recipeweave.compatibility_rule AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
