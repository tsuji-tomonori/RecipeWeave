-- 最終確認を一度だけ消費し、失敗時には全置換とともに取消す。
UPDATE recipeweave.backup_restore_intent SET consumed_at = CLOCK_TIMESTAMP()
WHERE
    id = %(intent_id)s AND user_id = %(actor_id)s AND body_sha256 = %(body_sha256)s
    AND current_revision = %(current_revision)s AND consumed_at IS NULL
    AND expires_at > CLOCK_TIMESTAMP()
RETURNING id;
