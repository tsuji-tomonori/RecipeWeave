-- 調理前の買い物確認を条件付き削除する。
-- 値は名前付きパラメータで束縛する。
DELETE FROM recipeweave.user_shopping_check AS t
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND t.user_id = %(actor_id)s
RETURNING
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
    t.xmin::TEXT AS etag;
