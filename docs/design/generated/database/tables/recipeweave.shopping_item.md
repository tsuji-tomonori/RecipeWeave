# テーブル仕様: recipeweave.shopping_item

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

買い物行

定義元: `database/migrations/002_relational_schema.sql:statement-571`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| session_id | uuid | 不可 | なし | なし | 対象調理 |
| total_id | uuid | 不可 | なし | なし | 需要行 |
| product_version_id | uuid | 可 | なし | なし | 購入SKU |
| net_shortage | numeric(20,6) | 不可 | なし | net_shortage &gt;= 0; net_shortage IS NULL OR net_shortage::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 在庫控除後の不足量 |
| package_count | integer | 可 | なし | package_count IS NULL OR package_count &gt;= 0 | 購入包装数 |
| surplus_amount | numeric(20,6) | 可 | なし | surplus_amount IS NULL OR surplus_amount &gt;= 0; surplus_amount IS NULL OR surplus_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 購入後余剰 |
| checked | boolean | 不可 | なし | なし | 購入済み |
| client_key | text | 可 | なし | なし | 画面操作の安定キー |
| checked_at | timestamptz | 可 | なし | なし | 購入確認日時 |
| archived | boolean | 不可 | FALSE | なし | 完了した買い物の保管状態 |

## 表制約

- `CHECK (net_shortage >= 0)`
- `CHECK (package_count IS NULL OR package_count >= 0)`
- `CHECK (surplus_amount IS NULL OR surplus_amount >= 0)`
- `CHECK (net_shortage IS NULL OR net_shortage::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (surplus_amount IS NULL OR surplus_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_shopping_item_session_id | False | (session_id) |
| ix_shopping_item_total_id | False | (total_id) |
| ix_shopping_item_product_version_id | False | (product_version_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_shopping_item_session_id | session_id | cooking_session(id) | CASCADE | RESTRICT | True |
| fk_shopping_item_total_id | total_id | ingredient_total(id) | RESTRICT | RESTRICT | True |
| fk_shopping_item_product_version_id | product_version_id | product_version(id) | RESTRICT | RESTRICT | True |

保持・所属領域: owned / 献立

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| export_backup | R | backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q010_export_tables.sql |
| preview_backup | D | backend/src/app/apis/backup/preview_backup/sql/q100_delete_shopping_item.sql |
| preview_backup | C | backend/src/app/apis/backup/preview_backup/sql/q200_insert_shopping_item.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q010_export_tables.sql |
| restore_backup | D | backend/src/app/apis/backup/restore_backup/sql/q100_delete_shopping_item.sql |
| restore_backup | C | backend/src/app/apis/backup/restore_backup/sql/q200_insert_shopping_item.sql |
| entity_shopping_item_create | C | backend/src/app/apis/entities/shopping_item_create/sql/001_create.sql |
| entity_shopping_item_delete | D | backend/src/app/apis/entities/shopping_item_delete/sql/001_delete.sql |
| entity_shopping_item_get | R | backend/src/app/apis/entities/shopping_item_get/sql/001_get.sql |
| entity_shopping_item_list | R | backend/src/app/apis/entities/shopping_item_list/sql/001_list.sql |
| entity_shopping_item_update | U | backend/src/app/apis/entities/shopping_item_update/sql/001_update.sql |
