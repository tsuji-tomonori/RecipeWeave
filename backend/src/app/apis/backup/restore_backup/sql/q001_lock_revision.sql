-- 本人の更新版をロックし、確認と置換の間の更新を検出する。
SELECT revision FROM recipeweave.workspace_revision
WHERE user_id = %(actor_id)s FOR UPDATE;
