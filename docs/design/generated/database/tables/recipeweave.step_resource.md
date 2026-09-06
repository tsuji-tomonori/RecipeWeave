# テーブル仕様: recipeweave.step_resource

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

工程の資源要求

定義元: `database/migrations/002_relational_schema.sql:statement-325`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| step_id | uuid | 不可 | なし | なし | 対象工程 |
| resource_type_id | uuid | 不可 | なし | なし | 要求種別 |
| quantity | integer | 不可 | なし | quantity &gt; 0 | 必要台数・人数 |
| capacity_min | numeric(20,6) | 可 | なし | capacity_min IS NULL OR capacity_min &gt; 0; capacity_min IS NULL OR capacity_min::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 必要最低容量 |
| exclusive | boolean | 不可 | なし | なし | 占有するか |

## 表制約

- `CHECK (quantity > 0)`
- `CHECK (capacity_min IS NULL OR capacity_min > 0)`
- `CHECK (capacity_min IS NULL OR capacity_min::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `UNIQUE (step_id, resource_type_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_step_resource_step_id | False | (step_id) |
| ix_step_resource_resource_type_id | False | (resource_type_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_step_resource_step_id | step_id | recipe_step(id) | RESTRICT | RESTRICT | True |
| fk_step_resource_resource_type_id | resource_type_id | resource_type(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 工程

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_step_resource_create | C | backend/src/app/apis/entities/step_resource_create/sql/001_create.sql |
| entity_step_resource_get | R | backend/src/app/apis/entities/step_resource_get/sql/001_get.sql |
| entity_step_resource_list | R | backend/src/app/apis/entities/step_resource_list/sql/001_list.sql |
| entity_step_resource_update | U | backend/src/app/apis/entities/step_resource_update/sql/001_update.sql |
| get_recipe | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| list_recipes | R | backend/src/app/apis/recipes/list_recipes/sql/001_select_recipes.sql |
| random_recipe | R | backend/src/app/apis/recipes/random_recipe/sql/001_random_recipe.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q022_requirements.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| preview_cooking_plan | R | backend/src/app/apis/workspace/preview_cooking_plan/sql/q003_requirements.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| preview_cooking_plan | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
