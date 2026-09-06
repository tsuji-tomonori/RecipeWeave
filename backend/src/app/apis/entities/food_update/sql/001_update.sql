-- 購入・利用食材概念を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.food AS t
SET
    code = %(code)s,
    name = %(name)s,
    kind = %(kind)s,
    parent_id = %(parent_id)s,
    release_id = %(release_id)s,
    status = %(status)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
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
