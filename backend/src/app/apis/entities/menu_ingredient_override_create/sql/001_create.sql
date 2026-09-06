-- 献立別材料確定を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.menu_ingredient_override AS t (
    id,
    menu_item_id,
    ingredient_line_id,
    selected,
    amount,
    form_id,
    product_version_id
)
VALUES (
    %(row_id)s,
    %(menu_item_id)s,
    %(ingredient_line_id)s,
    %(selected)s,
    %(amount)s,
    %(form_id)s,
    %(product_version_id)s
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
