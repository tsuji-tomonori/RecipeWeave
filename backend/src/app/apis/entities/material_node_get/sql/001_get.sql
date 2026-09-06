-- 材料・中間物ノードを取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.name,
    t.kind,
    t.ingredient_line_id,
    t.producer_step_id,
    t.amount,
    t.unit_id,
    t.xmin::TEXT AS etag
FROM recipeweave.material_node AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
