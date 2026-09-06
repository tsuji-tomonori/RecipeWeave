-- 列挙範囲・リース管理を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.template_id,
    t.start_ordinal,
    t.end_ordinal,
    t.next_ordinal,
    t.lease_owner,
    t.lease_expires_at,
    t.fence_token,
    t.state,
    t.xmin::TEXT AS etag
FROM recipeweave.generation_shard AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
