# テーブル仕様: recipeweave.menu

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

献立

定義元: `database/migrations/002_relational_schema.sql:statement-471`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| user_id | uuid | 不可 | なし | なし | 所有者 |
| name | text | 不可 | なし | LENGTH(BTRIM(name)) BETWEEN 1 AND 20000 | 献立名 |
| servings | numeric(20,6) | 不可 | なし | servings &gt; 0; servings IS NULL OR servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 標準人数 |
| revision | integer | 不可 | なし | revision &gt; 0 | 楽観ロック版 |

## 表制約

- `CHECK (servings > 0)`
- `CHECK (revision > 0)`
- `CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000)`
- `CHECK (servings IS NULL OR servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_menu_user_id | False | (user_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_menu_user_id | user_id | app_user(id) | CASCADE | RESTRICT | True |

保持・所属領域: owned / 献立

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_cooking_session_create | R | backend/src/app/apis/entities/cooking_session_create/sql/002_reference_menu_id.sql |
| entity_cooking_session_delete | R | backend/src/app/apis/entities/cooking_session_delete/sql/001_delete.sql |
| entity_cooking_session_get | R | backend/src/app/apis/entities/cooking_session_get/sql/001_get.sql |
| entity_cooking_session_list | R | backend/src/app/apis/entities/cooking_session_list/sql/001_list.sql |
| entity_cooking_session_update | R | backend/src/app/apis/entities/cooking_session_update/sql/001_update.sql |
| entity_cooking_session_update | R | backend/src/app/apis/entities/cooking_session_update/sql/002_reference_menu_id.sql |
| entity_ingredient_total_get | R | backend/src/app/apis/entities/ingredient_total_get/sql/001_get.sql |
| entity_ingredient_total_list | R | backend/src/app/apis/entities/ingredient_total_list/sql/001_list.sql |
| entity_menu_create | C | backend/src/app/apis/entities/menu_create/sql/001_create.sql |
| entity_menu_delete | D | backend/src/app/apis/entities/menu_delete/sql/001_delete.sql |
| entity_menu_get | R | backend/src/app/apis/entities/menu_get/sql/001_get.sql |
| entity_menu_ingredient_override_create | R | backend/src/app/apis/entities/menu_ingredient_override_create/sql/002_reference_menu_item_id.sql |
| entity_menu_ingredient_override_delete | R | backend/src/app/apis/entities/menu_ingredient_override_delete/sql/001_delete.sql |
| entity_menu_ingredient_override_get | R | backend/src/app/apis/entities/menu_ingredient_override_get/sql/001_get.sql |
| entity_menu_ingredient_override_list | R | backend/src/app/apis/entities/menu_ingredient_override_list/sql/001_list.sql |
| entity_menu_ingredient_override_update | R | backend/src/app/apis/entities/menu_ingredient_override_update/sql/001_update.sql |
| entity_menu_ingredient_override_update | R | backend/src/app/apis/entities/menu_ingredient_override_update/sql/002_reference_menu_item_id.sql |
| entity_menu_item_create | R | backend/src/app/apis/entities/menu_item_create/sql/002_reference_menu_id.sql |
| entity_menu_item_create | R | backend/src/app/apis/entities/menu_item_create/sql/003_reference_recipe_version_id.sql |
| entity_menu_item_delete | R | backend/src/app/apis/entities/menu_item_delete/sql/001_delete.sql |
| entity_menu_item_get | R | backend/src/app/apis/entities/menu_item_get/sql/001_get.sql |
| entity_menu_item_list | R | backend/src/app/apis/entities/menu_item_list/sql/001_list.sql |
| entity_menu_item_update | R | backend/src/app/apis/entities/menu_item_update/sql/001_update.sql |
| entity_menu_item_update | R | backend/src/app/apis/entities/menu_item_update/sql/002_reference_menu_id.sql |
| entity_menu_item_update | R | backend/src/app/apis/entities/menu_item_update/sql/003_reference_recipe_version_id.sql |
| entity_menu_list | R | backend/src/app/apis/entities/menu_list/sql/001_list.sql |
| entity_menu_update | U | backend/src/app/apis/entities/menu_update/sql/001_update.sql |
| entity_resource_reservation_create | R | backend/src/app/apis/entities/resource_reservation_create/sql/002_reference_task_id.sql |
| entity_resource_reservation_delete | R | backend/src/app/apis/entities/resource_reservation_delete/sql/001_delete.sql |
| entity_resource_reservation_get | R | backend/src/app/apis/entities/resource_reservation_get/sql/001_get.sql |
| entity_resource_reservation_list | R | backend/src/app/apis/entities/resource_reservation_list/sql/001_list.sql |
| entity_resource_reservation_update | R | backend/src/app/apis/entities/resource_reservation_update/sql/001_update.sql |
| entity_resource_reservation_update | R | backend/src/app/apis/entities/resource_reservation_update/sql/002_reference_task_id.sql |
| entity_session_task_create | R | backend/src/app/apis/entities/session_task_create/sql/002_reference_session_id.sql |
| entity_session_task_create | R | backend/src/app/apis/entities/session_task_create/sql/003_reference_menu_item_id.sql |
| entity_session_task_delete | R | backend/src/app/apis/entities/session_task_delete/sql/001_delete.sql |
| entity_session_task_get | R | backend/src/app/apis/entities/session_task_get/sql/001_get.sql |
| entity_session_task_list | R | backend/src/app/apis/entities/session_task_list/sql/001_list.sql |
| entity_session_task_update | R | backend/src/app/apis/entities/session_task_update/sql/001_update.sql |
| entity_session_task_update | R | backend/src/app/apis/entities/session_task_update/sql/002_reference_session_id.sql |
| entity_session_task_update | R | backend/src/app/apis/entities/session_task_update/sql/003_reference_menu_item_id.sql |
| entity_shopping_item_create | R | backend/src/app/apis/entities/shopping_item_create/sql/002_reference_session_id.sql |
| entity_shopping_item_create | R | backend/src/app/apis/entities/shopping_item_create/sql/003_reference_total_id.sql |
| entity_shopping_item_delete | R | backend/src/app/apis/entities/shopping_item_delete/sql/001_delete.sql |
| entity_shopping_item_get | R | backend/src/app/apis/entities/shopping_item_get/sql/001_get.sql |
| entity_shopping_item_list | R | backend/src/app/apis/entities/shopping_item_list/sql/001_list.sql |
| entity_shopping_item_update | R | backend/src/app/apis/entities/shopping_item_update/sql/001_update.sql |
| entity_shopping_item_update | R | backend/src/app/apis/entities/shopping_item_update/sql/002_reference_session_id.sql |
| entity_shopping_item_update | R | backend/src/app/apis/entities/shopping_item_update/sql/003_reference_total_id.sql |
| entity_task_dependency_create | R | backend/src/app/apis/entities/task_dependency_create/sql/002_reference_before_task_id.sql |
| entity_task_dependency_create | R | backend/src/app/apis/entities/task_dependency_create/sql/003_reference_after_task_id.sql |
| entity_task_dependency_delete | R | backend/src/app/apis/entities/task_dependency_delete/sql/001_delete.sql |
| entity_task_dependency_get | R | backend/src/app/apis/entities/task_dependency_get/sql/001_get.sql |
| entity_task_dependency_list | R | backend/src/app/apis/entities/task_dependency_list/sql/001_list.sql |
| entity_task_dependency_update | R | backend/src/app/apis/entities/task_dependency_update/sql/001_update.sql |
| entity_task_dependency_update | R | backend/src/app/apis/entities/task_dependency_update/sql/002_reference_before_task_id.sql |
| entity_task_dependency_update | R | backend/src/app/apis/entities/task_dependency_update/sql/003_reference_after_task_id.sql |
| entity_user_recipe_event_create | R | backend/src/app/apis/entities/user_recipe_event_create/sql/003_reference_recipe_version_id.sql |
| get_recipe | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| add_menu_item | C | backend/src/app/apis/workspace/add_menu_item/sql/q012_menu.sql |
| add_menu_item | U | backend/src/app/apis/workspace/add_menu_item/sql/q015_advance_menu.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q001_current.sql |
| create_cooking_session | C | backend/src/app/apis/workspace/create_cooking_session/sql/q012_menu.sql |
| create_cooking_session | U | backend/src/app/apis/workspace/create_cooking_session/sql/q015_advance_menu.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q030_menu_revision.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/delete_menu_item/sql/q001_delete_item.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/update_cooking_session/sql/q001_current.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/update_cooking_session/sql/q002_tasks.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/update_cooking_session/sql/q003_progress.sql |
| update_menu_item | R | backend/src/app/apis/workspace/update_menu_item/sql/q001_delete_item.sql |
| update_menu_item | C | backend/src/app/apis/workspace/update_menu_item/sql/q012_menu.sql |
| update_menu_item | U | backend/src/app/apis/workspace/update_menu_item/sql/q015_advance_menu.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| preview_cooking_plan | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
