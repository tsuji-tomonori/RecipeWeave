# テーブル仕様: recipeweave.ingredient_total

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

献立材料集計結果

定義元: `database/migrations/002_relational_schema.sql:statement-549`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| session_id | uuid | 不可 | なし | なし | 固定計算対象 |
| form_id | uuid | 不可 | なし | なし | 合算可能な形態 |
| product_version_id | uuid | 可 | なし | なし | 商品固定 |
| unit_id | uuid | 不可 | なし | なし | 基準単位 |
| required_amount | numeric(20,6) | 不可 | なし | required_amount &gt;= 0; required_amount IS NULL OR required_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 必要量 |
| quality | text | 不可 | なし | LENGTH(BTRIM(quality)) BETWEEN 1 AND 20000; quality IN ('measured', 'manufacturer', 'reference', 'estimated', 'unknown') | 最も低い入力精度 |
| calculation_version | text | 不可 | なし | LENGTH(BTRIM(calculation_version)) BETWEEN 1 AND 20000 | 計算器版 |
| actual_amount | numeric(20,6) | 可 | なし |  actual_amount IS NULL OR (actual_amount &gt;= 0 AND actual_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))  | 利用者が確定した実使用量。不明はNULL |
| consumption_outcome | text | 不可 | 'not_requested' |  consumption_outcome IN ('not_requested', 'applied', 'insufficient', 'unknown', 'incompatible')  | 未要求・反映済み・在庫不足・数量不明・単位不一致の結果 |

## 表制約

- `CHECK (required_amount >= 0)`
- `CHECK (required_amount IS NULL OR required_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (LENGTH(BTRIM(quality)) BETWEEN 1 AND 20000)`
- `CHECK (quality IN ('measured', 'manufacturer', 'reference', 'estimated', 'unknown'))`
- `CHECK (LENGTH(BTRIM(calculation_version)) BETWEEN 1 AND 20000)`
- `CHECK ( actual_amount IS NULL OR (actual_amount >= 0 AND actual_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')) )`
- `CHECK ( consumption_outcome IN ('not_requested', 'applied', 'insufficient', 'unknown', 'incompatible') )`
- `UNIQUE NULLS NOT DISTINCT (session_id, form_id, product_version_id, unit_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_ingredient_total_session_id | False | (session_id) |
| ix_ingredient_total_form_id | False | (form_id) |
| ix_ingredient_total_product_version_id | False | ( product_version_id ) |
| ix_ingredient_total_unit_id | False | (unit_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_ingredient_total_session_id | session_id | cooking_session(id) | CASCADE | RESTRICT | True |
| fk_ingredient_total_form_id | form_id | food_form(id) | RESTRICT | RESTRICT | True |
| fk_ingredient_total_product_version_id | product_version_id | product_version(id) | RESTRICT | RESTRICT | True |
| fk_ingredient_total_unit_id | unit_id | unit(id) | RESTRICT | RESTRICT | True |

保持・所属領域: transient / 献立

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| export_backup | R | backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q010_export_tables.sql |
| preview_backup | D | backend/src/app/apis/backup/preview_backup/sql/q100_delete_ingredient_total.sql |
| preview_backup | C | backend/src/app/apis/backup/preview_backup/sql/q200_insert_ingredient_total.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q010_export_tables.sql |
| restore_backup | D | backend/src/app/apis/backup/restore_backup/sql/q100_delete_ingredient_total.sql |
| restore_backup | C | backend/src/app/apis/backup/restore_backup/sql/q200_insert_ingredient_total.sql |
| entity_ingredient_total_get | R | backend/src/app/apis/entities/ingredient_total_get/sql/001_get.sql |
| entity_ingredient_total_list | R | backend/src/app/apis/entities/ingredient_total_list/sql/001_list.sql |
| entity_shopping_item_create | R | backend/src/app/apis/entities/shopping_item_create/sql/003_reference_total_id.sql |
| entity_shopping_item_update | R | backend/src/app/apis/entities/shopping_item_update/sql/003_reference_total_id.sql |
| create_cooking_session | C | backend/src/app/apis/workspace/create_cooking_session/sql/q029_total.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/update_cooking_session/sql/q006_totals.sql |
| update_cooking_session | U | backend/src/app/apis/workspace/update_cooking_session/sql/q010_outcome.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
