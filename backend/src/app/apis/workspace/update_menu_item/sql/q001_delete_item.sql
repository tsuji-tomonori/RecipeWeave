-- 本人の現在の献立の料理を外す。調理中の入力は専用の献立版へ保存する。
DELETE FROM recipeweave.menu_item
WHERE
    id = %(row_id)s AND menu_id = %(menu_id)s
    AND EXISTS (
        SELECT 1 FROM recipeweave.menu AS m
        WHERE m.id = %(menu_id)s AND m.user_id = %(user_id)s
    )
RETURNING id;
