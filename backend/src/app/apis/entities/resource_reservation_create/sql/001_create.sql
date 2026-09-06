-- 資源の予約を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.resource_reservation AS t (
    id,
    task_id,
    resource_id,
    start_s,
    end_s,
    quantity
)
VALUES (
    %(row_id)s,
    %(task_id)s,
    %(resource_id)s,
    %(start_s)s,
    %(end_s)s,
    %(quantity)s
)
RETURNING
    t.id,
    t.created_at,
    t.task_id,
    t.resource_id,
    t.start_s,
    t.end_s,
    t.quantity,
    t.xmin::TEXT AS etag;
