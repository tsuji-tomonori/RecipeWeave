-- 料理同一性上の食品を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.food_identity AS t (
    id,
    code,
    name,
    normalizer_version
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(name)s,
    %(normalizer_version)s
)
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.normalizer_version,
    t.xmin::TEXT AS etag;
