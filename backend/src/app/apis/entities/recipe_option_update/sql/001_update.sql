-- 版の分類・特徴を条件付き更新する。
-- 値は名前付きパラメータで束縛する。
UPDATE recipeweave.recipe_option AS t
SET
    recipe_version_id = %(recipe_version_id)s,
    option_id = %(option_id)s
WHERE
    t.id = %(row_id)s
    AND t.xmin::TEXT = %(expected_etag)s
    AND TRUE
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.option_id,
    t.xmin::TEXT AS etag;
