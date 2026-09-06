-- 本人へ発行したバックアップの証拠。本文を保存せず、削除後も匿名化した発行記録を保持するを取得する。
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
    t.id = %(row_id)s
    AND t.user_id = %(actor_id)s;
