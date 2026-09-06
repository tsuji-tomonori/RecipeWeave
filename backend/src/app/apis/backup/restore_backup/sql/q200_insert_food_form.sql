-- 検証済みバックアップの食材形態を元IDと全列で復元する。
INSERT INTO recipeweave.food_form (
    id,
    created_at,
    food_id,
    name,
    state,
    base_unit_id,
    quantity_basis,
    status
) VALUES (
    %(id)s,
    %(created_at)s,
    %(food_id)s,
    %(name)s,
    %(state)s,
    %(base_unit_id)s,
    %(quantity_basis)s,
    %(status)s
);
