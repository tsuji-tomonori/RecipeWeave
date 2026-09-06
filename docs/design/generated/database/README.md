# 物理テーブル一覧

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

実DDLで作られる表だけを掲載する。JSON状態内の配列や将来の正規化テーブルは物理表として数えない。

| テーブル | 意味 | 列数 | 定義元 |
|---|---|---|---|
| [recipeweave.schema_migrations](tables/recipeweave.schema_migrations.md) | 移行IDとchecksum、完了時刻を保持する運用台帳。DDLの構造確認が成功した後に記録し、アプリAPIから更新しない。 | 3 | database/migrate.py:117 |
| [recipeweave.user_state](tables/recipeweave.user_state.md) | 認証済み利用者ごとに、検証済みの端末状態とサーバー側の版を保持する。レシピ正規化DBの将来設計とは別の、Dev同期用の物理テーブル。 | 4 | database/migrations/001_user_state.sql |

[ER図](ER.md) / [APIとのCRUD](../api/CRUD.md)
