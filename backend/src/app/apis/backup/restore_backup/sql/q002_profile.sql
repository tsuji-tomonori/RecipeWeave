-- 認証主体・状態を含めず、復元できる本人の表示設定だけを読む。
SELECT
    locale,
    timezone
FROM recipeweave.app_user
WHERE id = %(actor_id)s;
