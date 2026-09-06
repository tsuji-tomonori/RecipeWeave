# テーブル仕様: recipeweave.recipe_step

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

調理工程ノード

定義元: `database/migrations/002_relational_schema.sql:statement-268`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| recipe_version_id | uuid | 不可 | なし | なし | 所属版 |
| step_no | integer | 不可 | なし | step_no &gt; 0 | 表示順（依存順とは別） |
| operation_id | uuid | 不可 | なし | なし | 標準動作 |
| instruction | text | 不可 | なし | LENGTH(BTRIM(instruction)) BETWEEN 1 AND 20000; CHAR_LENGTH(instruction) &lt;= 5000 | 個別補足 |
| attention | text | 不可 | なし | LENGTH(BTRIM(attention)) BETWEEN 1 AND 20000; attention IN ('active', 'monitored', 'passive') | 作業者拘束 |
| duration_min_s | integer | 不可 | なし | duration_min_s &gt;= 0; duration_max_s &gt;= duration_min_s | 所要秒下限 |
| duration_max_s | integer | 不可 | なし | duration_max_s &gt;= duration_min_s | 所要秒上限 |
| scaling_rule_id | uuid | 不可 | なし | なし | 時間の人数変更規則 |
| completion_cue | text | 不可 | なし | LENGTH(BTRIM(completion_cue)) BETWEEN 1 AND 20000 | 実測・目視の終了条件 |
| title | text | 可 | なし | CHAR_LENGTH(title) &lt;= 500 | 工程の短い見出し |

## 表制約

- `CHECK (step_no > 0)`
- `CHECK (duration_min_s >= 0)`
- `CHECK (duration_max_s >= duration_min_s)`
- `CHECK (LENGTH(BTRIM(instruction)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(attention)) BETWEEN 1 AND 20000)`
- `CHECK (attention IN ('active', 'monitored', 'passive'))`
- `CHECK (LENGTH(BTRIM(completion_cue)) BETWEEN 1 AND 20000)`
- `CHECK (CHAR_LENGTH(title) <= 500)`
- `CHECK (CHAR_LENGTH(instruction) <= 5000)`
- `UNIQUE (recipe_version_id, step_no)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_recipe_step_recipe_version_id | False | (recipe_version_id) |
| ix_recipe_step_operation_id | False | (operation_id) |
| ix_recipe_step_scaling_rule_id | False | (scaling_rule_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_recipe_step_recipe_version_id | recipe_version_id | recipe_version(id) | RESTRICT | RESTRICT | True |
| fk_recipe_step_operation_id | operation_id | operation(id) | RESTRICT | RESTRICT | True |
| fk_recipe_step_scaling_rule_id | scaling_rule_id | scaling_rule(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 工程

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_recipe_step_create | C | backend/src/app/apis/entities/recipe_step_create/sql/001_create.sql |
| entity_recipe_step_get | R | backend/src/app/apis/entities/recipe_step_get/sql/001_get.sql |
| entity_recipe_step_list | R | backend/src/app/apis/entities/recipe_step_list/sql/001_list.sql |
| entity_recipe_step_update | U | backend/src/app/apis/entities/recipe_step_update/sql/001_update.sql |
| get_recipe | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| list_recipes | R | backend/src/app/apis/recipes/list_recipes/sql/001_select_recipes.sql |
| random_recipe | R | backend/src/app/apis/recipes/random_recipe/sql/001_random_recipe.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q020_steps.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q021_dependencies.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q022_requirements.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| preview_cooking_plan | R | backend/src/app/apis/workspace/preview_cooking_plan/sql/q001_steps.sql |
| preview_cooking_plan | R | backend/src/app/apis/workspace/preview_cooking_plan/sql/q002_dependencies.sql |
| preview_cooking_plan | R | backend/src/app/apis/workspace/preview_cooking_plan/sql/q003_requirements.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| preview_cooking_plan | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
