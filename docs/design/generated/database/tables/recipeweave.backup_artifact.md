# テーブル仕様: recipeweave.backup_artifact

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

本人へ発行したバックアップの証拠。本文を保存せず、削除後も匿名化した発行記録を保持する

定義元: `database/migrations/004_backup_restore.sql:statement-1`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | バックアップ本文に含める不変の発行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | サーバーによる発行日時（UTC） |
| user_id | uuid | 可 | なし | なし | 発行先の本人。利用者消去後だけNULLへ匿名化する |
| body_sha256 | text | 不可 | なし | body_sha256 ~ '^[0-9a-f]{64}$' | 発行識別子を含む正規化済み本文全体のSHA-256 |
| format_version | integer | 不可 | なし | format_version = 2 | 対応するバックアップの形式版。現在は2 |

## 表制約

- `CHECK (body_sha256 ~ '^[0-9a-f]{64}$')`
- `CHECK (format_version = 2)`
- `UNIQUE (user_id, body_sha256, format_version)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_backup_artifact_user_id | False | (user_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_backup_artifact_user_id | user_id | app_user(id) | SET NULL | RESTRICT | True |

保持・所属領域: audit / バックアップ復元

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| export_backup | C | backend/src/app/apis/backup/export_backup/sql/q021_issue_artifact.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q020_artifact.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q020_artifact.sql |
| entity_backup_artifact_get | R | backend/src/app/apis/entities/backup_artifact_get/sql/001_get.sql |
| entity_backup_artifact_list | R | backend/src/app/apis/entities/backup_artifact_list/sql/001_list.sql |
