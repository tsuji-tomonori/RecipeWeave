-- 検証済みバックアップの献立別材料確定を元IDと全列で復元する。
INSERT INTO recipeweave.menu_ingredient_override (
    id,
    created_at,
    menu_item_id,
    ingredient_line_id,
    selected,
    amount,
    form_id,
    product_version_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(menu_item_id)s,
    %(ingredient_line_id)s,
    %(selected)s,
    %(amount)s,
    %(form_id)s,
    %(product_version_id)s
);
