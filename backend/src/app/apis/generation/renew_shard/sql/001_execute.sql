-- 本人・フェンス・有効期限が一致する現ワーカーだけがリースを延長する。
UPDATE recipeweave.generation_shard AS s
SET lease_expires_at = NOW() + MAKE_INTERVAL(secs => %(lease_seconds)s)
WHERE
    s.id = %(row_id)s AND s.lease_owner = %(lease_owner)s
    AND s.fence_token = %(expected_fence)s AND s.lease_expires_at > NOW()
    AND s.state = 'running'
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
