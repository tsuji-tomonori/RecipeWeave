# テーブル仕様: recipeweave.backup_restore_intent

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

復元内容の確認記録。本人・本文・確認時の更新版・期限を固定し、一度だけ消費する

定義元: `database/migrations/004_backup_restore.sql:statement-10`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 確認画面へ返す不変の復元確認識別子 |
| created_at | timestamptz | 不可 | NOW() | expires_at &gt; created_at AND expires_at &lt;= created_at + INTERVAL '15 minutes'; consumed_at IS NULL OR (consumed_at &gt;= created_at AND consumed_at &lt; expires_at) | 復元内容を検証して確認記録を発行した日時（UTC） |
| user_id | uuid | 可 | なし | なし | 復元する本人。利用者消去後だけNULLへ匿名化する |
| artifact_id | uuid | 不可 | なし | なし | 本人へ発行したバックアップ証拠の識別子 |
| body_sha256 | text | 不可 | なし | body_sha256 ~ '^[0-9a-f]{64}$' | 確認した本文全体のSHA-256。発行記録と一致する |
| current_revision | bigint | 不可 | なし | current_revision &gt;= 0 | 確認時の現在データの更新版。復元直前にも同じ値であることを検査する |
| expires_at | timestamptz | 不可 | なし | expires_at &gt; created_at AND expires_at &lt;= created_at + INTERVAL '15 minutes'; consumed_at IS NULL OR (consumed_at &gt;= created_at AND consumed_at &lt; expires_at) | 確認の有効期限。発行から最大15分 |
| consumed_at | timestamptz | 可 | なし | consumed_at IS NULL OR (consumed_at &gt;= created_at AND consumed_at &lt; expires_at) | 復元と同一トランザクションで確定する使用日時。取消・再使用は不可 |

## 表制約

- `CHECK (body_sha256 ~ '^[0-9a-f]{64}$')`
- `CHECK (current_revision >= 0)`
- `CHECK (expires_at > created_at AND expires_at <= created_at + INTERVAL '15 minutes')`
- `CHECK (consumed_at IS NULL OR (consumed_at >= created_at AND consumed_at < expires_at))`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_backup_restore_intent_user_id | False | (user_id) |
| ix_backup_restore_intent_artifact_id | False | ( artifact_id ) |
| ix_backup_restore_intent_pending | False | (user_id, expires_at) WHERE consumed_at IS NULL |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_backup_restore_intent_user_id | user_id | app_user(id) | SET NULL | RESTRICT | True |
| fk_backup_restore_intent_artifact_id | artifact_id | backup_artifact(id) | RESTRICT | RESTRICT | True |

保持・所属領域: audit / バックアップ復元

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| preview_backup | C | backend/src/app/apis/backup/preview_backup/sql/q022_issue_intent.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q023_lock_intent.sql |
| restore_backup | U | backend/src/app/apis/backup/restore_backup/sql/q024_consume_intent.sql |
| entity_backup_restore_intent_get | R | backend/src/app/apis/entities/backup_restore_intent_get/sql/001_get.sql |
| entity_backup_restore_intent_list | R | backend/src/app/apis/entities/backup_restore_intent_list/sql/001_list.sql |
