-- 古いバックアップ版へ戻さず、ロックした本人の現行版を一度だけ進める。
UPDATE recipeweave.workspace_revision SET revision = revision + 1
WHERE user_id = %(actor_id)s;
