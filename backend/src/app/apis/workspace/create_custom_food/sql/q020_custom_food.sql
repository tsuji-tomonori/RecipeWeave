-- 私有カタログへ本人の独自食材を登録する。
INSERT INTO recipeweave.food (id, code, name, kind, parent_id, release_id, status, owner_id)
VALUES (
    %(food_id)s, %(code)s, %(name)s, 'basic', NULL, %(release_id)s, 'active', %(user_id)s
) RETURNING id;
