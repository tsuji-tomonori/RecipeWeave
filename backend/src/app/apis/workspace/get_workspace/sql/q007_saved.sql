-- 保存と解除の追記イベントから、料理ごとの現在状態を導出する。
SELECT ranked.recipe_id FROM (
    SELECT
        rv.recipe_id,
        ev.kind,
        ROW_NUMBER()
            OVER (
                PARTITION BY rv.recipe_id
                ORDER BY ev.occurred_at DESC, ev.created_at DESC, ev.id DESC
            )
            AS rank
    FROM recipeweave.user_recipe_event AS ev
    INNER JOIN recipeweave.recipe_version AS rv ON ev.recipe_version_id = rv.id
    WHERE ev.user_id = %(user_id)s AND ev.kind IN ('liked', 'disliked')
) AS ranked
WHERE ranked.rank = 1 AND ranked.kind = 'liked'
ORDER BY ranked.recipe_id;
