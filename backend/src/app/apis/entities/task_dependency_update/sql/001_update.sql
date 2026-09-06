-- 献立展開後依存を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.task_dependency AS t
SET
    before_task_id = %(before_task_id)s,
    after_task_id = %(after_task_id)s,
    min_lag_s = %(min_lag_s)s,
    max_lag_s = %(max_lag_s)s,
    reason = %(reason)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND EXISTS (
        SELECT owner_0.id
        FROM recipeweave.session_task AS owner_0
        WHERE
            owner_0.id = t.before_task_id
            AND EXISTS (
                SELECT owner_1.id
                FROM recipeweave.cooking_session AS owner_1
                WHERE
                    owner_1.id = owner_0.session_id
                    AND EXISTS (
                        SELECT owner_2.id
                        FROM recipeweave.menu AS owner_2
                        WHERE
                            owner_2.id = owner_1.menu_id
                            AND owner_2.user_id = %(actor_id)s
                    )
            )
    )
RETURNING
    t.id,
    t.created_at,
    t.before_task_id,
    t.after_task_id,
    t.min_lag_s,
    t.max_lag_s,
    t.reason,
    t.xmin::TEXT AS etag;
