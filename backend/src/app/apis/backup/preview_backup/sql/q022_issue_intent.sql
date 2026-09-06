-- 検証した本文と現在版を15分間の最終確認へ結び付ける。
INSERT INTO recipeweave.backup_restore_intent
(id, user_id, artifact_id, body_sha256, current_revision, expires_at)
VALUES (
    %(intent_id)s, %(actor_id)s, %(artifact_id)s, %(body_sha256)s,
    %(current_revision)s, CURRENT_TIMESTAMP + INTERVAL '15 minutes'
)
RETURNING id, expires_at;
