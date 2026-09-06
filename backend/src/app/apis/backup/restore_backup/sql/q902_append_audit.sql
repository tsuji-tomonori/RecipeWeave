-- 復元本文を複製せず、全置換した本人キーのハッシュだけを監査へ残す。
INSERT INTO recipeweave.audit_event
(id, actor_id, action, entity_type, entity_key_hash, reason, occurred_at)
VALUES (
    %(row_id)s, %(actor_id)s, 'backup/restore', 'workspace', %(key_hash)s,
    '本人が確認した全置換復元', CURRENT_TIMESTAMP
);
