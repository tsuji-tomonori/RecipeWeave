-- 個人本文を複製せず、同じ業務トランザクションで変更履歴を追記する。
INSERT INTO recipeweave.audit_event (
    id, actor_id, action, entity_type, entity_key_hash, reason, occurred_at
)
VALUES (
    %(row_id)s, %(actor_id)s, %(action)s, %(entity_type)s,
    %(entity_key_hash)s, 'APIによる正規化データ操作', NOW()
)
RETURNING id;
