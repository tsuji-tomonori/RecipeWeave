# テーブル仕様: recipeweave.menu_item

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

献立の料理

定義元: `database/migrations/002_relational_schema.sql:statement-479`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| menu_id | uuid | 不可 | なし | なし | 献立 |
| recipe_version_id | uuid | 不可 | なし | なし | 固定レシピ版 |
| servings | numeric(20,6) | 不可 | なし | servings &gt; 0; servings IS NULL OR servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | その料理を作る人数 |
| role_option_id | uuid | 不可 | なし | なし | 主菜等 |
| position | integer | 不可 | なし | position &gt; 0 | 表示順 |

## 表制約

- `CHECK (servings > 0)`
- `CHECK (position > 0)`
- `CHECK (servings IS NULL OR servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `UNIQUE (menu_id, position)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_menu_item_menu_id | False | (menu_id) |
| ix_menu_item_recipe_version_id | False | (recipe_version_id) |
| ix_menu_item_role_option_id | False | (role_option_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_menu_item_menu_id | menu_id | menu(id) | CASCADE | RESTRICT | True |
| fk_menu_item_recipe_version_id | recipe_version_id | recipe_version(id) | RESTRICT | RESTRICT | True |
| fk_menu_item_role_option_id | role_option_id | axis_option(id) | RESTRICT | RESTRICT | True |

保持・所属領域: owned / 献立

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| export_backup | R | backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q100_delete_menu_ingredient_override.sql |
| preview_backup | D | backend/src/app/apis/backup/preview_backup/sql/q100_delete_menu_item.sql |
| preview_backup | C | backend/src/app/apis/backup/preview_backup/sql/q200_insert_menu_item.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q010_export_tables.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q100_delete_menu_ingredient_override.sql |
| restore_backup | D | backend/src/app/apis/backup/restore_backup/sql/q100_delete_menu_item.sql |
| restore_backup | C | backend/src/app/apis/backup/restore_backup/sql/q200_insert_menu_item.sql |
| entity_menu_ingredient_override_create | R | backend/src/app/apis/entities/menu_ingredient_override_create/sql/002_reference_menu_item_id.sql |
| entity_menu_ingredient_override_delete | R | backend/src/app/apis/entities/menu_ingredient_override_delete/sql/001_delete.sql |
| entity_menu_ingredient_override_get | R | backend/src/app/apis/entities/menu_ingredient_override_get/sql/001_get.sql |
| entity_menu_ingredient_override_list | R | backend/src/app/apis/entities/menu_ingredient_override_list/sql/001_list.sql |
| entity_menu_ingredient_override_update | R | backend/src/app/apis/entities/menu_ingredient_override_update/sql/001_update.sql |
| entity_menu_ingredient_override_update | R | backend/src/app/apis/entities/menu_ingredient_override_update/sql/002_reference_menu_item_id.sql |
| entity_menu_item_create | C | backend/src/app/apis/entities/menu_item_create/sql/001_create.sql |
| entity_menu_item_create | R | backend/src/app/apis/entities/menu_item_create/sql/003_reference_recipe_version_id.sql |
| entity_menu_item_delete | D | backend/src/app/apis/entities/menu_item_delete/sql/001_delete.sql |
| entity_menu_item_get | R | backend/src/app/apis/entities/menu_item_get/sql/001_get.sql |
| entity_menu_item_list | R | backend/src/app/apis/entities/menu_item_list/sql/001_list.sql |
| entity_menu_item_update | U | backend/src/app/apis/entities/menu_item_update/sql/001_update.sql |
| entity_menu_item_update | R | backend/src/app/apis/entities/menu_item_update/sql/003_reference_recipe_version_id.sql |
| entity_session_task_create | R | backend/src/app/apis/entities/session_task_create/sql/003_reference_menu_item_id.sql |
| entity_session_task_update | R | backend/src/app/apis/entities/session_task_update/sql/003_reference_menu_item_id.sql |
| entity_user_recipe_event_create | R | backend/src/app/apis/entities/user_recipe_event_create/sql/003_reference_recipe_version_id.sql |
| get_recipe | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| add_menu_item | C,R | backend/src/app/apis/workspace/add_menu_item/sql/q013_insert_item.sql |
| create_cooking_session | C,R | backend/src/app/apis/workspace/create_cooking_session/sql/q013_insert_item.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q020_steps.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q021_dependencies.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q022_requirements.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q024_ingredients.sql |
| delete_menu_item | D | backend/src/app/apis/workspace/delete_menu_item/sql/q001_delete_item.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| update_menu_item | D | backend/src/app/apis/workspace/update_menu_item/sql/q001_delete_item.sql |
| update_menu_item | C,R | backend/src/app/apis/workspace/update_menu_item/sql/q013_insert_item.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| preview_cooking_plan | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
