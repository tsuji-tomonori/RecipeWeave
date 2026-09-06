-- 検証済みバックアップの購入・利用食材概念を元IDと全列で復元する。
INSERT INTO recipeweave.food (
    id,
    created_at,
    code,
    name,
    kind,
    parent_id,
    release_id,
    status,
    owner_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(code)s,
    %(name)s,
    %(kind)s,
    %(parent_id)s,
    %(release_id)s,
    %(status)s,
    %(owner_id)s
);
