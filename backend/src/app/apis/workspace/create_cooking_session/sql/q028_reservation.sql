-- 本人の設備を必要な時間と数だけ予約する。
INSERT INTO recipeweave.resource_reservation (id, task_id, resource_id, start_s, end_s, quantity)
VALUES (%(row_id)s, %(task_id)s, %(resource_id)s, %(start)s, %(end)s, %(quantity)s);
