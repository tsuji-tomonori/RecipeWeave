-- 完了済み工程の巻戻しをせず進行位置と状態を更新する。
UPDATE recipeweave.cooking_session SET status = %(status)s, current_task_index = %(index)s
WHERE
    id = %(session_id)s AND status IN ('cooking', 'paused')
    AND EXISTS (
        SELECT 1 FROM recipeweave.menu AS m
        WHERE m.id = cooking_session.menu_id AND m.user_id = %(user_id)s
    )
RETURNING id;
