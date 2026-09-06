# テーブル仕様: recipeweave.user_pantry_food

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

利用者が常備すると設定した食材

定義元: `database/migrations/003_service_operations.sql:statement-37`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| user_id | uuid | 不可 | なし | なし | 所有者 |
| food_id | uuid | 不可 | なし | なし | 常備食材 |

## 表制約

- `UNIQUE (user_id, food_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_user_pantry_food_user_id | False | (user_id) |
| ix_user_pantry_food_food_id | False | (food_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_user_pantry_food_user_id | user_id | app_user(id) | CASCADE | RESTRICT | True |
| fk_user_pantry_food_food_id | food_id | food(id) | RESTRICT | RESTRICT | True |

保持・所属領域: owned / 利用者操作

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| export_backup | R | backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q010_export_tables.sql |
| preview_backup | D | backend/src/app/apis/backup/preview_backup/sql/q100_delete_user_pantry_food.sql |
| preview_backup | C | backend/src/app/apis/backup/preview_backup/sql/q200_insert_user_pantry_food.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q010_export_tables.sql |
| restore_backup | D | backend/src/app/apis/backup/restore_backup/sql/q100_delete_user_pantry_food.sql |
| restore_backup | C | backend/src/app/apis/backup/restore_backup/sql/q200_insert_user_pantry_food.sql |
| entity_user_pantry_food_create | C | backend/src/app/apis/entities/user_pantry_food_create/sql/001_create.sql |
| entity_user_pantry_food_delete | D | backend/src/app/apis/entities/user_pantry_food_delete/sql/001_delete.sql |
| entity_user_pantry_food_get | R | backend/src/app/apis/entities/user_pantry_food_get/sql/001_get.sql |
| entity_user_pantry_food_list | R | backend/src/app/apis/entities/user_pantry_food_list/sql/001_list.sql |
| entity_user_pantry_food_update | U | backend/src/app/apis/entities/user_pantry_food_update/sql/001_update.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| put_settings | D | backend/src/app/apis/workspace/put_settings/sql/q002_clear_pantry.sql |
| put_settings | C | backend/src/app/apis/workspace/put_settings/sql/q005_pantry.sql |
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
