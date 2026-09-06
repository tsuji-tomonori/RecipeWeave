-- バックアップ本文を保存せず、本人への発行根拠だけを記録する。
INSERT INTO recipeweave.backup_artifact (id, user_id, body_sha256, format_version)
VALUES (%(artifact_id)s, %(actor_id)s, %(body_sha256)s, 2);
