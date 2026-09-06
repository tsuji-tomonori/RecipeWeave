-- 材料・中間物ノードを作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.material_node AS t (
    id,
    recipe_version_id,
    name,
    kind,
    ingredient_line_id,
    producer_step_id,
    amount,
    unit_id
)
VALUES (
    %(row_id)s,
    %(recipe_version_id)s,
    %(name)s,
    %(kind)s,
    %(ingredient_line_id)s,
    %(producer_step_id)s,
    %(amount)s,
    %(unit_id)s
)
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
