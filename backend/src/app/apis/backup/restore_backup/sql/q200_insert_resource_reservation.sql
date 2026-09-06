-- 検証済みバックアップの資源の予約を元IDと全列で復元する。
INSERT INTO recipeweave.resource_reservation (
    id,
    created_at,
    task_id,
    resource_id,
    start_s,
    end_s,
    quantity
) VALUES (
    %(id)s,
    %(created_at)s,
    %(task_id)s,
    %(resource_id)s,
    %(start_s)s,
    %(end_s)s,
    %(quantity)s
);
