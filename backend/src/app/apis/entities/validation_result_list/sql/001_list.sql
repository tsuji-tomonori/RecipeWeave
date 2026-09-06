-- 公開前評価結果を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.rule_id,
    t.state,
    t.evidence,
    t.validator_version,
    t.evaluated_at,
    t.xmin::TEXT AS etag
FROM recipeweave.validation_result AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
