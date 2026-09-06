-- 道具・設備・作業者種別を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.resource_type AS t
SET
    code = %(code)s,
    name = %(name)s,
    capacity_unit_id = %(capacity_unit_id)s,
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
    t.capacity_unit_id,
    t.status,
    t.xmin::TEXT AS etag;
