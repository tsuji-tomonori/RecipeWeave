-- 発行した本人と本文digestが一致する根拠だけを認可に使う。
SELECT id FROM recipeweave.backup_artifact
WHERE
    id = %(artifact_id)s AND user_id = %(actor_id)s
    AND body_sha256 = %(body_sha256)s AND format_version = 2;
