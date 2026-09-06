-- 待機または失効した範囲を排他取得し、新しいフェンスでリースを開始する。
WITH selected AS (
    SELECT id FROM recipeweave.generation_shard
    WHERE
        (state = 'queued' OR (state = 'running' AND lease_expires_at <= NOW()))
        AND (%(template_id)s::UUID IS NULL OR template_id = %(template_id)s)
    ORDER BY created_at, id
    LIMIT 1
    FOR UPDATE SKIP LOCKED
)

UPDATE recipeweave.generation_shard AS s
SET
    lease_owner = %(lease_owner)s,
    lease_expires_at = NOW() + MAKE_INTERVAL(secs => %(lease_seconds)s),
    fence_token = s.fence_token + 1,
    state = 'running'
FROM selected
WHERE s.id = selected.id
RETURNING
    s.id,
    s.created_at,
    s.template_id,
    s.start_ordinal,
    s.end_ordinal,
    s.next_ordinal,
    s.lease_owner,
    s.lease_expires_at,
    s.fence_token,
    s.state,
    s.xmin::TEXT AS etag;
