# テーブル仕様: recipeweave.recipe

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

レシピ同一性

定義元: `database/migrations/002_relational_schema.sql:statement-178`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| title | text | 不可 | なし | LENGTH(BTRIM(title)) BETWEEN 1 AND 20000; CHAR_LENGTH(title) &lt;= 500 | 代表名 |
| family_option_id | uuid | 不可 | なし | なし | 料理ファミリ |
| status | text | 不可 | なし | status &lt;&gt; 'withdrawn' OR NULLIF(BTRIM(withdrawal_reason), '') IS NOT NULL; LENGTH(BTRIM(status)) BETWEEN 1 AND 20000; status IN ('draft', 'published', 'withdrawn') | 公開状態 |
| withdrawal_reason | text | 可 | なし | status &lt;&gt; 'withdrawn' OR NULLIF(BTRIM(withdrawal_reason), '') IS NOT NULL | 取下げ理由 |

## 表制約

- `CHECK (status <> 'withdrawn' OR NULLIF(BTRIM(withdrawal_reason), '') IS NOT NULL)`
- `CHECK (LENGTH(BTRIM(title)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000)`
- `CHECK (status IN ('draft', 'published', 'withdrawn'))`
- `CHECK (CHAR_LENGTH(title) <= 500)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_recipe_family_option_id | False | (family_option_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_recipe_family_option_id | family_option_id | axis_option(id) | RESTRICT | RESTRICT | True |

保持・所属領域: catalog / レシピ

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_menu_item_create | R | backend/src/app/apis/entities/menu_item_create/sql/003_reference_recipe_version_id.sql |
| entity_menu_item_update | R | backend/src/app/apis/entities/menu_item_update/sql/003_reference_recipe_version_id.sql |
| entity_recipe_create | C | backend/src/app/apis/entities/recipe_create/sql/001_create.sql |
| entity_recipe_get | R | backend/src/app/apis/entities/recipe_get/sql/001_get.sql |
| entity_recipe_list | R | backend/src/app/apis/entities/recipe_list/sql/001_list.sql |
| entity_recipe_update | U | backend/src/app/apis/entities/recipe_update/sql/001_update.sql |
| entity_user_recipe_event_create | R | backend/src/app/apis/entities/user_recipe_event_create/sql/003_reference_recipe_version_id.sql |
| get_recipe | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| list_recipes | R | backend/src/app/apis/recipes/list_recipes/sql/001_select_recipes.sql |
| random_recipe | R | backend/src/app/apis/recipes/random_recipe/sql/001_random_recipe.sql |
| add_menu_item | R | backend/src/app/apis/workspace/add_menu_item/sql/q010_recipe.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q010_recipe.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| save_recipe | R | backend/src/app/apis/workspace/save_recipe/sql/q001_recipe.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/unsave_recipe/sql/q001_recipe.sql |
| update_menu_item | R | backend/src/app/apis/workspace/update_menu_item/sql/q010_recipe.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
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
