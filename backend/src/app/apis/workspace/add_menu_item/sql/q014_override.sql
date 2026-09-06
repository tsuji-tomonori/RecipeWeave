-- 利用者が確認した確定分量だけを元の材料行へ結び付ける。
INSERT INTO recipeweave.menu_ingredient_override (
    id, menu_item_id, ingredient_line_id, selected, amount, form_id, product_version_id
)
VALUES (%(row_id)s, %(item_id)s, %(ingredient_id)s, %(selected)s, %(amount)s, NULL, NULL);
