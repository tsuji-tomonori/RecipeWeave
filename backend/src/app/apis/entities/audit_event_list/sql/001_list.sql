-- 変更・公開監査を一覧取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.actor_id,
    t.action,
    t.entity_type,
    t.entity_key_hash,
    t.reason,
    t.occurred_at,
    t.xmin::TEXT AS etag
FROM recipeweave.audit_event AS t
WHERE
    TRUE
    AND (%(after_id)s::UUID IS NULL OR t.id > %(after_id)s)
ORDER BY t.id
LIMIT %(page_limit)s;
