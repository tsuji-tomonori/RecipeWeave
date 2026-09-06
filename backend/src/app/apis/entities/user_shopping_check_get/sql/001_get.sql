-- 調理前の買い物確認を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.user_id,
    t.key,
    t.signature,
    t.food_id,
    t.amount,
    t.unit_id,
    t.checked_at,
    t.archived,
    t.xmin::TEXT AS etag
FROM recipeweave.user_shopping_check AS t
WHERE
    t.id = %(row_id)s
    AND t.user_id = %(actor_id)s;
