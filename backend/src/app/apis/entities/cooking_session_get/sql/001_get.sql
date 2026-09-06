-- 調理計画実行を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.menu_id,
    t.menu_revision,
    t.status,
    t.target_at,
    t.planner_version,
    t.input_snapshot,
    t.input_hash,
    t.current_task_index,
    t.xmin::TEXT AS etag
FROM recipeweave.cooking_session AS t
WHERE
    t.id = %(row_id)s
    AND EXISTS (
        SELECT owner_0.id
        FROM recipeweave.menu AS owner_0
        WHERE
            owner_0.id = t.menu_id
            AND owner_0.user_id = %(actor_id)s
    );
