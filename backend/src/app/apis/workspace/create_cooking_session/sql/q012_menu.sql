-- 現在の献立を初回だけ作成し、所有者を固定する。
INSERT INTO recipeweave.menu (id, user_id, name, servings, revision)
VALUES (%(menu_id)s, %(user_id)s, %(name)s, 2, 1) ON CONFLICT (id) DO NOTHING;
