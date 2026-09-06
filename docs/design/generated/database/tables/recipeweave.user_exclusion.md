# テーブル仕様: recipeweave.user_exclusion

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

避けたい食材・物質

定義元: `database/migrations/002_relational_schema.sql:statement-454`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| user_id | uuid | 不可 | なし | なし | 利用者 |
| food_id | uuid | 可 | なし | NUM_NONNULLS(food_id, allergen_id) = 1 | 食材 |
| allergen_id | uuid | 可 | なし | NUM_NONNULLS(food_id, allergen_id) = 1 | アレルゲン |
| strict | boolean | 不可 | なし | なし | 不明も除外するか |

## 表制約

- `CHECK (NUM_NONNULLS(food_id, allergen_id) = 1)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_user_exclusion_user_id | False | (user_id) |
| ix_user_exclusion_food_id | False | (food_id) |
| ix_user_exclusion_allergen_id | False | (allergen_id) |
| uq_user_exclusion_0 | True | ( user_id, food_id ) WHERE food_id IS NOT NULL |
| uq_user_exclusion_1 | True | ( user_id, allergen_id ) WHERE allergen_id IS NOT NULL |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_user_exclusion_user_id | user_id | app_user(id) | CASCADE | RESTRICT | True |
| fk_user_exclusion_food_id | food_id | food(id) | RESTRICT | RESTRICT | True |
| fk_user_exclusion_allergen_id | allergen_id | allergen(id) | RESTRICT | RESTRICT | True |

保持・所属領域: owned / 利用者

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| export_backup | R | backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q010_export_tables.sql |
| preview_backup | D | backend/src/app/apis/backup/preview_backup/sql/q100_delete_user_exclusion.sql |
| preview_backup | C | backend/src/app/apis/backup/preview_backup/sql/q200_insert_user_exclusion.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q010_export_tables.sql |
| restore_backup | D | backend/src/app/apis/backup/restore_backup/sql/q100_delete_user_exclusion.sql |
| restore_backup | C | backend/src/app/apis/backup/restore_backup/sql/q200_insert_user_exclusion.sql |
| entity_user_exclusion_create | C | backend/src/app/apis/entities/user_exclusion_create/sql/001_create.sql |
| entity_user_exclusion_delete | D | backend/src/app/apis/entities/user_exclusion_delete/sql/001_delete.sql |
| entity_user_exclusion_get | R | backend/src/app/apis/entities/user_exclusion_get/sql/001_get.sql |
| entity_user_exclusion_list | R | backend/src/app/apis/entities/user_exclusion_list/sql/001_list.sql |
| entity_user_exclusion_update | U | backend/src/app/apis/entities/user_exclusion_update/sql/001_update.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| put_settings | D | backend/src/app/apis/workspace/put_settings/sql/q001_clear_exclusion.sql |
| put_settings | C | backend/src/app/apis/workspace/put_settings/sql/q004_exclusion.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
