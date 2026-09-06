-- 食材形態を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.food_form AS t (
    id,
    food_id,
    name,
    state,
    base_unit_id,
    quantity_basis,
    status
)
VALUES (
    %(row_id)s,
    %(food_id)s,
    %(name)s,
    %(state)s,
    %(base_unit_id)s,
    %(quantity_basis)s,
    %(status)s
)
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
