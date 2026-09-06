-- 現ワーカーのフェンスを確認し、範囲内の単調な進捗だけを確定する。
UPDATE recipeweave.generation_shard AS s
SET next_ordinal = %(next_ordinal)s, state = %(state)s
WHERE
    s.id = %(row_id)s AND s.lease_owner = %(lease_owner)s
    AND s.fence_token = %(expected_fence)s AND s.lease_expires_at > NOW()
    AND s.state = 'running' AND %(next_ordinal)s >= s.next_ordinal
    AND %(next_ordinal)s <= s.end_ordinal
    AND (%(state)s <> 'done' OR %(next_ordinal)s = s.end_ordinal)
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
