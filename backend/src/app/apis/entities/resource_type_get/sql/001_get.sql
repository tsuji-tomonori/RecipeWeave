-- 道具・設備・作業者種別を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.capacity_unit_id,
    t.status,
    t.xmin::TEXT AS etag
FROM recipeweave.resource_type AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
