-- 復元内容の確認記録。本人・本文・確認時の更新版・期限を固定し、一度だけ消費するを一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.user_id,
    t.artifact_id,
    t.body_sha256,
    t.current_revision,
    t.expires_at,
    t.consumed_at,
    t.xmin::TEXT AS etag
FROM recipeweave.backup_restore_intent AS t
WHERE
    t.user_id = %(actor_id)s
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
