-- 購買食品から同一性への対応を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.food_identity_member AS t (
    id,
    food_id,
    identity_id,
    normalizer_version,
    reason
)
VALUES (
    %(row_id)s,
    %(food_id)s,
    %(identity_id)s,
    %(normalizer_version)s,
    %(reason)s
)
RETURNING
    t.id,
    t.created_at,
    t.food_id,
    t.identity_id,
    t.normalizer_version,
    t.reason,
    t.xmin::TEXT AS etag;
