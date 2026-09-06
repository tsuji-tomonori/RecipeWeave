# テーブル仕様: recipeweave.pantry_lot

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

手持ち食材ロット

定義元: `database/migrations/002_relational_schema.sql:statement-560`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| user_id | uuid | 不可 | なし | なし | 所有者 |
| form_id | uuid | 不可 | なし | なし | 食材形態 |
| product_version_id | uuid | 可 | なし | なし | 商品版 |
| amount | numeric(20,6) | 可 | なし | amount &gt;= 0; amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity');  (quantity_quality = 'known' AND amount IS NOT NULL) OR (quantity_quality = 'unknown' AND amount IS NULL)  | 残量 |
| unit_id | uuid | 不可 | なし | なし | 単位 |
| expires_on | date | 可 | なし | なし | 表示期限 |
| opened_at | timestamptz | 可 | なし | なし | 開封時点 |
| location | text | 不可 | 'fridge' |  location IN ('fridge', 'freezer', 'pantry')  | 冷蔵・冷凍・常温の保管場所 |
| priority | text | 不可 | 'normal' |  priority IN ('normal', 'use_first')  | 先に使う優先指定 |
| status | text | 不可 | 'active' |  status IN ('active', 'deleted', 'undone')  | 在庫の有効・削除・レシート取消状態 |
| source_import_id | uuid | 可 | なし | なし | 登録元レシート |
| quantity_quality | text | 不可 | 'known' |  (quantity_quality = 'known' AND amount IS NOT NULL) OR (quantity_quality = 'unknown' AND amount IS NULL)  | 数量の確定・不明 |
| original_form_id | uuid | 可 | なし | なし | 登録時の食材形態 |
| original_amount | numeric(20,6) | 可 | なし |  original_amount IS NULL OR (original_amount &gt;= 0 AND original_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))  | 登録時数量。不明はNULL |
| original_unit_id | uuid | 可 | なし | なし | 登録時単位 |
| updated_at | timestamptz | 不可 | NOW() | なし | 最終編集日時 |
| edited | boolean | 不可 | FALSE | なし | 登録後の編集有無 |

## 表制約

- `CHECK (amount >= 0)`
- `CHECK (amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK ( location IN ('fridge', 'freezer', 'pantry') )`
- `CHECK ( priority IN ('normal', 'use_first') )`
- `CHECK ( status IN ('active', 'deleted', 'undone') )`
- `CHECK ( (quantity_quality = 'known' AND amount IS NOT NULL) OR (quantity_quality = 'unknown' AND amount IS NULL) )`
- `CHECK ( original_amount IS NULL OR (original_amount >= 0 AND original_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')) )`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_pantry_lot_user_id | False | (user_id) |
| ix_pantry_lot_form_id | False | (form_id) |
| ix_pantry_lot_product_version_id | False | (product_version_id) |
| ix_pantry_lot_unit_id | False | (unit_id) |
| ix_pantry_lot_source_import_id | False | (source_import_id) |
| ix_pantry_lot_original_form_id | False | (original_form_id) |
| ix_pantry_lot_original_unit_id | False | (original_unit_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_pantry_lot_user_id | user_id | app_user(id) | CASCADE | RESTRICT | True |
| fk_pantry_lot_form_id | form_id | food_form(id) | RESTRICT | RESTRICT | True |
| fk_pantry_lot_product_version_id | product_version_id | product_version(id) | RESTRICT | RESTRICT | True |
| fk_pantry_lot_unit_id | unit_id | unit(id) | RESTRICT | RESTRICT | True |
| fk_pantry_lot_source_import_id | source_import_id | receipt_import(id) | SET NULL | RESTRICT | True |
| fk_pantry_lot_original_form_id | original_form_id | food_form(id) | RESTRICT | RESTRICT | True |
| fk_pantry_lot_original_unit_id | original_unit_id | unit(id) | RESTRICT | RESTRICT | True |

保持・所属領域: owned / 献立

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_pantry_lot_create | C | backend/src/app/apis/entities/pantry_lot_create/sql/001_create.sql |
| entity_pantry_lot_delete | D | backend/src/app/apis/entities/pantry_lot_delete/sql/001_delete.sql |
| entity_pantry_lot_get | R | backend/src/app/apis/entities/pantry_lot_get/sql/001_get.sql |
| entity_pantry_lot_list | R | backend/src/app/apis/entities/pantry_lot_list/sql/001_list.sql |
| entity_pantry_lot_update | U | backend/src/app/apis/entities/pantry_lot_update/sql/001_update.sql |
| entity_receipt_line_create | R | backend/src/app/apis/entities/receipt_line_create/sql/003_reference_pantry_lot_id.sql |
| entity_receipt_line_update | R | backend/src/app/apis/entities/receipt_line_update/sql/003_reference_pantry_lot_id.sql |
| commit_receipt | C | backend/src/app/apis/workspace/commit_receipt/sql/q002_insert_lot.sql |
| create_pantry_lot | C | backend/src/app/apis/workspace/create_pantry_lot/sql/q002_insert_lot.sql |
| delete_pantry_lot | U | backend/src/app/apis/workspace/delete_pantry_lot/sql/q001_delete_lot.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| undo_receipt | U | backend/src/app/apis/workspace/undo_receipt/sql/q002_eligible_lots.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/update_cooking_session/sql/q007_available.sql |
| update_cooking_session | U | backend/src/app/apis/workspace/update_cooking_session/sql/q008_consume.sql |
| update_pantry_lot | U | backend/src/app/apis/workspace/update_pantry_lot/sql/q002_update_lot.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
