-- 購入・利用食材概念を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.food AS t (
    id,
    code,
    name,
    kind,
    parent_id,
    release_id,
    status
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(name)s,
    %(kind)s,
    %(parent_id)s,
    %(release_id)s,
    %(status)s
)
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.kind,
    t.parent_id,
    t.release_id,
    t.status,
    t.owner_id,
    t.xmin::TEXT AS etag;
