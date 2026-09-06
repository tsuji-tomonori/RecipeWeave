# テーブル仕様: recipeweave.recipe_option

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

版の分類・特徴

定義元: `database/migrations/002_relational_schema.sql:statement-200`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| recipe_version_id | uuid | 不可 | なし | なし | 対象版 |
| option_id | uuid | 不可 | なし | なし | 特徴値 |

## 表制約

- `UNIQUE (recipe_version_id, option_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_recipe_option_recipe_version_id | False | (recipe_version_id) |
| ix_recipe_option_option_id | False | (option_id) |
| ix_recipe_option_search_0 | False | (option_id, recipe_version_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_recipe_option_recipe_version_id | recipe_version_id | recipe_version(id) | RESTRICT | RESTRICT | True |
| fk_recipe_option_option_id | option_id | axis_option(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / レシピ

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_recipe_option_create | C | backend/src/app/apis/entities/recipe_option_create/sql/001_create.sql |
| entity_recipe_option_get | R | backend/src/app/apis/entities/recipe_option_get/sql/001_get.sql |
| entity_recipe_option_list | R | backend/src/app/apis/entities/recipe_option_list/sql/001_list.sql |
| entity_recipe_option_update | U | backend/src/app/apis/entities/recipe_option_update/sql/001_update.sql |
| get_recipe | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| list_recipes | R | backend/src/app/apis/recipes/list_recipes/sql/001_select_recipes.sql |
| random_recipe | R | backend/src/app/apis/recipes/random_recipe/sql/001_random_recipe.sql |
| add_menu_item | R | backend/src/app/apis/workspace/add_menu_item/sql/q010_recipe.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q010_recipe.sql |
| update_menu_item | R | backend/src/app/apis/workspace/update_menu_item/sql/q010_recipe.sql |
| preview_cooking_plan | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
