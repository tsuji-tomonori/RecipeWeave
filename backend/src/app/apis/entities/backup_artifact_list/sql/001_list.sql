-- 本人へ発行したバックアップの証拠。本文を保存せず、削除後も匿名化した発行記録を保持するを一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.user_id,
    t.body_sha256,
    t.format_version,
    t.xmin::TEXT AS etag
FROM recipeweave.backup_artifact AS t
WHERE
    t.user_id = %(actor_id)s
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
