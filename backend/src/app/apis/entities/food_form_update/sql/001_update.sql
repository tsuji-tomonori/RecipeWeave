-- 食材形態を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.food_form AS t
SET
    food_id = %(food_id)s,
    name = %(name)s,
    state = %(state)s,
    base_unit_id = %(base_unit_id)s,
    quantity_basis = %(quantity_basis)s,
    status = %(status)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.food_id,
    t.name,
    t.state,
    t.base_unit_id,
    t.quantity_basis,
    t.status,
    t.xmin::TEXT AS etag;
