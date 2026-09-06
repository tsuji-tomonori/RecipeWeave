-- 参照先のレシート読取・在庫登録の処理単位が同じ利用者に属することを検証する。
SELECT t.id FROM recipeweave.receipt_import AS t
WHERE
    t.id = %(reference_id)s
    AND t.user_id = %(actor_id)s;
