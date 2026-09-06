-- 公開検索用文書を取得する。
-- 値は名前付きパラメータで束縛する。
SELECT
    t.id,
    t.created_at,
    t.recipe_id,
    t.published_version_id,
    t.projection_version,
    t.display_title,
    t.food_identity_ids,
    t.facet_option_ids,
    t.search_text,
    t.eligible,
    t.source_hash,
    t.projected_at,
    t.xmin::TEXT AS etag
FROM recipeweave.recipe_search_document AS t
WHERE
    t.id = %(row_id)s
    AND TRUE;
