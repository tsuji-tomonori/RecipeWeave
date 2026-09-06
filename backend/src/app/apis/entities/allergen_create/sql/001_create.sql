-- アレルゲン概念を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.allergen AS t (
    id,
    code,
    name,
    source_id
)
VALUES (
    %(row_id)s,
    %(code)s,
    %(name)s,
    %(source_id)s
)
RETURNING
    t.id,
    t.created_at,
    t.code,
    t.name,
    t.source_id,
    t.xmin::TEXT AS etag;
