-- 道具・設備・作業者種別を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.resource_type AS t (
    id,
    code,
    name,
    capacity_unit_id,
    status
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(name)s,
    %(capacity_unit_id)s,
    %(status)s
)
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.capacity_unit_id,
    t.status,
    t.xmin::TEXT AS etag;
