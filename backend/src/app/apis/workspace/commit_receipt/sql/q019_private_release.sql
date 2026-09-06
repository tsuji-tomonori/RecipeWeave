-- 共通の公開版と分離し、本人が編集する私有カタログを初回だけ用意する。
INSERT INTO recipeweave.catalog_release (id, version, manifest_hash, published_at, owner_id)
VALUES (%(release_id)s, %(version)s, %(manifest)s, NULL, %(user_id)s) ON CONFLICT (id) DO NOTHING;
