# テーブル仕様: recipeweave.receipt_line

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

レシートの商品候補と確定した在庫の対応

定義元: `database/migrations/003_service_operations.sql:statement-12`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| import_id | uuid | 不可 | なし | なし | レシート処理 |
| line_no | integer | 不可 | なし | line_no &gt; 0 | レシート内の表示順 |
| raw_name | text | 不可 | なし | なし | 利用者が確認できる商品原表記 |
| form_id | uuid | 可 | なし | decision &lt;&gt; 'accepted' OR form_id IS NOT NULL | 確定した食材形態 |
| product_version_id | uuid | 可 | なし | なし | 確定した商品版 |
| amount | numeric(20,6) | 可 | なし | amount IS NULL OR amount &gt; 0; amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'); (amount IS NULL) OR unit_id IS NOT NULL | 数量。不明はNULL |
| unit_id | uuid | 可 | なし | (amount IS NULL) OR unit_id IS NOT NULL | 確定数量の単位 |
| decision | text | 不可 | 'unresolved' | decision IN ('accepted', 'skipped', 'unresolved'); decision &lt;&gt; 'accepted' OR form_id IS NOT NULL | accepted/skipped/unresolved |
| pantry_lot_id | uuid | 可 | なし | なし | 登録したロット |

## 表制約

- `CHECK (line_no > 0)`
- `CHECK (decision IN ('accepted', 'skipped', 'unresolved'))`
- `CHECK (amount IS NULL OR amount > 0)`
- `CHECK (amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK ((amount IS NULL) OR unit_id IS NOT NULL)`
- `CHECK (decision <> 'accepted' OR form_id IS NOT NULL)`
- `UNIQUE (import_id, line_no)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_receipt_line_import_id | False | (import_id) |
| ix_receipt_line_form_id | False | (form_id) |
| ix_receipt_line_product_version_id | False | (product_version_id) |
| ix_receipt_line_unit_id | False | (unit_id) |
| ix_receipt_line_pantry_lot_id | False | (pantry_lot_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_receipt_line_import_id | import_id | receipt_import(id) | CASCADE | RESTRICT | True |
| fk_receipt_line_form_id | form_id | food_form(id) | RESTRICT | RESTRICT | True |
| fk_receipt_line_product_version_id | product_version_id | product_version(id) | RESTRICT | RESTRICT | True |
| fk_receipt_line_unit_id | unit_id | unit(id) | RESTRICT | RESTRICT | True |
| fk_receipt_line_pantry_lot_id | pantry_lot_id | pantry_lot(id) | SET NULL | RESTRICT | True |

保持・所属領域: owned / 利用者操作

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| export_backup | R | backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q010_export_tables.sql |
| preview_backup | D | backend/src/app/apis/backup/preview_backup/sql/q100_delete_receipt_line.sql |
| preview_backup | C | backend/src/app/apis/backup/preview_backup/sql/q200_insert_receipt_line.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q010_export_tables.sql |
| restore_backup | D | backend/src/app/apis/backup/restore_backup/sql/q100_delete_receipt_line.sql |
| restore_backup | C | backend/src/app/apis/backup/restore_backup/sql/q200_insert_receipt_line.sql |
| entity_receipt_line_create | C | backend/src/app/apis/entities/receipt_line_create/sql/001_create.sql |
| entity_receipt_line_delete | D | backend/src/app/apis/entities/receipt_line_delete/sql/001_delete.sql |
| entity_receipt_line_get | R | backend/src/app/apis/entities/receipt_line_get/sql/001_get.sql |
| entity_receipt_line_list | R | backend/src/app/apis/entities/receipt_line_list/sql/001_list.sql |
| entity_receipt_line_update | U | backend/src/app/apis/entities/receipt_line_update/sql/001_update.sql |
| commit_receipt | C | backend/src/app/apis/workspace/commit_receipt/sql/q005_line.sql |
