# テーブル仕様: recipeweave.receipt_import

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

レシート読取・在庫登録の処理単位

定義元: `database/migrations/003_service_operations.sql:statement-1`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| user_id | uuid | 不可 | なし | なし | 所有者 |
| file_sha256 | char(64) | 可 | なし | なし | 画像本文のSHA256。本文はDBに保存しない |
| idempotency_key | text | 不可 | なし | なし | 本人内で一意の再送防止キー |
| status | text | 不可 | 'draft' | status IN ('draft', 'committed', 'reverted'); status &lt;&gt; 'committed' OR committed_at IS NOT NULL; status &lt;&gt; 'reverted' OR (committed_at IS NOT NULL AND reverted_at IS NOT NULL) | draft/committed/revertedの状態 |
| revision | bigint | 不可 | 1 | revision &gt;= 1 | 楽観ロック版 |
| committed_at | timestamptz | 可 | なし | status &lt;&gt; 'committed' OR committed_at IS NOT NULL; status &lt;&gt; 'reverted' OR (committed_at IS NOT NULL AND reverted_at IS NOT NULL) | 在庫へ登録した日時 |
| reverted_at | timestamptz | 可 | なし | status &lt;&gt; 'reverted' OR (committed_at IS NOT NULL AND reverted_at IS NOT NULL) | 登録取消日時 |
| undo_preserved_count | integer | 不可 | 0 |  undo_preserved_count &gt;= 0  | レシート取消時に編集・消費済みとして残した在庫件数 |

## 表制約

- `CHECK (status IN ('draft', 'committed', 'reverted'))`
- `CHECK (revision >= 1)`
- `CHECK (status <> 'committed' OR committed_at IS NOT NULL)`
- `CHECK (status <> 'reverted' OR (committed_at IS NOT NULL AND reverted_at IS NOT NULL))`
- `CHECK ( undo_preserved_count >= 0 )`
- `UNIQUE (user_id, idempotency_key)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_receipt_import_user_id | False | (user_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_receipt_import_user_id | user_id | app_user(id) | CASCADE | RESTRICT | True |

保持・所属領域: owned / 利用者操作

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| export_backup | R | backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q010_export_tables.sql |
| preview_backup | D | backend/src/app/apis/backup/preview_backup/sql/q100_delete_receipt_import.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q100_delete_receipt_line.sql |
| preview_backup | C | backend/src/app/apis/backup/preview_backup/sql/q200_insert_receipt_import.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q010_export_tables.sql |
| restore_backup | D | backend/src/app/apis/backup/restore_backup/sql/q100_delete_receipt_import.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q100_delete_receipt_line.sql |
| restore_backup | C | backend/src/app/apis/backup/restore_backup/sql/q200_insert_receipt_import.sql |
| entity_pantry_lot_create | R | backend/src/app/apis/entities/pantry_lot_create/sql/003_reference_source_import_id.sql |
| entity_pantry_lot_update | R | backend/src/app/apis/entities/pantry_lot_update/sql/003_reference_source_import_id.sql |
| entity_receipt_import_create | C | backend/src/app/apis/entities/receipt_import_create/sql/001_create.sql |
| entity_receipt_import_delete | D | backend/src/app/apis/entities/receipt_import_delete/sql/001_delete.sql |
| entity_receipt_import_get | R | backend/src/app/apis/entities/receipt_import_get/sql/001_get.sql |
| entity_receipt_import_list | R | backend/src/app/apis/entities/receipt_import_list/sql/001_list.sql |
| entity_receipt_import_update | U | backend/src/app/apis/entities/receipt_import_update/sql/001_update.sql |
| entity_receipt_line_create | R | backend/src/app/apis/entities/receipt_line_create/sql/002_reference_import_id.sql |
| entity_receipt_line_delete | R | backend/src/app/apis/entities/receipt_line_delete/sql/001_delete.sql |
| entity_receipt_line_get | R | backend/src/app/apis/entities/receipt_line_get/sql/001_get.sql |
| entity_receipt_line_list | R | backend/src/app/apis/entities/receipt_line_list/sql/001_list.sql |
| entity_receipt_line_update | R | backend/src/app/apis/entities/receipt_line_update/sql/001_update.sql |
| entity_receipt_line_update | R | backend/src/app/apis/entities/receipt_line_update/sql/002_reference_import_id.sql |
| commit_receipt | R | backend/src/app/apis/workspace/commit_receipt/sql/q003_duplicate.sql |
| commit_receipt | C | backend/src/app/apis/workspace/commit_receipt/sql/q004_import.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
| undo_receipt | R | backend/src/app/apis/workspace/undo_receipt/sql/q001_import.sql |
| undo_receipt | U | backend/src/app/apis/workspace/undo_receipt/sql/q003_revert.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/update_pantry_lot/sql/q002_update_lot.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql |
