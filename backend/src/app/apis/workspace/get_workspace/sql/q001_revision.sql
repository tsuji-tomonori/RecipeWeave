-- 複数表の読取り中に本人の業務更新が割り込まないよう共有ロックする。
SELECT revision FROM recipeweave.workspace_revision
WHERE user_id = %(user_id)s FOR SHARE;
