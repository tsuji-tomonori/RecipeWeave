-- 材料・中間物ノードを条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.material_node AS t
SET
    recipe_version_id = %(recipe_version_id)s,
    name = %(name)s,
    kind = %(kind)s,
    ingredient_line_id = %(ingredient_line_id)s,
    producer_step_id = %(producer_step_id)s,
    amount = %(amount)s,
    unit_id = %(unit_id)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.name,
    t.kind,
    t.ingredient_line_id,
    t.producer_step_id,
    t.amount,
    t.unit_id,
    t.xmin::TEXT AS etag;
