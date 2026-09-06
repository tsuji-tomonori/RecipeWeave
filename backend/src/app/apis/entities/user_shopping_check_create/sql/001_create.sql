-- 調理前の買い物確認を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.user_shopping_check AS t (
    id,
    user_id,
    key,
    signature,
    food_id,
    amount,
    unit_id,
    checked_at,
    archived
)
VALUES (
    %(row_id)s,
    %(user_id)s,
    %(key)s,
    %(signature)s,
    %(food_id)s,
    %(amount)s,
    %(unit_id)s,
    %(checked_at)s,
    %(archived)s
)
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
