-- 版の分類・特徴を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.option_id,
    t.xmin::TEXT AS etag
FROM recipeweave.recipe_option AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
