-- 購入・利用食材概念を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.kind,
    t.parent_id,
    t.release_id,
    t.status,
    t.owner_id,
    t.xmin::TEXT AS etag
FROM recipeweave.food AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
