-- 版の分類・特徴を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.recipe_option AS t (
    id,
    recipe_version_id,
    option_id
)
VALUES (
    %(row_id)s,
    %(recipe_version_id)s,
    %(option_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.recipe_version_id,
    t.option_id,
    t.xmin::TEXT AS etag;
