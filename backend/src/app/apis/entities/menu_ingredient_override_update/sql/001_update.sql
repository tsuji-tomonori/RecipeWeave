-- 献立別材料確定を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.menu_ingredient_override AS t
SET
    menu_item_id = %(menu_item_id)s,
    ingredient_line_id = %(ingredient_line_id)s,
    selected = %(selected)s,
    amount = %(amount)s,
    form_id = %(form_id)s,
    product_version_id = %(product_version_id)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND EXISTS (
        SELECT owner_0.id
        FROM recipeweave.menu_item AS owner_0
        WHERE
            owner_0.id = t.menu_item_id
            AND EXISTS (
                SELECT owner_1.id
                FROM recipeweave.menu AS owner_1
                WHERE
                    owner_1.id = owner_0.menu_id
                    AND owner_1.user_id = %(actor_id)s
            )
    )
RETURNING
    t.id,
    t.created_at,
    t.menu_item_id,
    t.ingredient_line_id,
    t.selected,
    t.amount,
    t.form_id,
    t.product_version_id,
    t.xmin::TEXT AS etag;
