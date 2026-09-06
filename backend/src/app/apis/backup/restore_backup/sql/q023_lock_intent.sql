-- 本人・本文・版が一致する未使用かつ期限内の確認をロックする。
SELECT id FROM recipeweave.backup_restore_intent
WHERE
    id = %(intent_id)s AND user_id = %(actor_id)s AND artifact_id = %(artifact_id)s
    AND body_sha256 = %(body_sha256)s AND current_revision = %(current_revision)s
    AND consumed_at IS NULL AND expires_at > CLOCK_TIMESTAMP()
FOR UPDATE;
