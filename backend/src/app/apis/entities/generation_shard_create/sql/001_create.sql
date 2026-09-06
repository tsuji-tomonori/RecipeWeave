-- 列挙範囲・リース管理を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.generation_shard AS t (
    id,
    template_id,
    start_ordinal,
    end_ordinal,
    next_ordinal,
    lease_owner,
    lease_expires_at,
    fence_token,
    state
)
VALUES (
    %(row_id)s,
    %(template_id)s,
    %(start_ordinal)s,
    %(end_ordinal)s,
    %(next_ordinal)s,
    %(lease_owner)s,
    %(lease_expires_at)s,
    %(fence_token)s,
    %(state)s
)
RETURNING
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
    t.xmin::TEXT AS etag;
