# テーブル仕様: recipeweave.recipe_version

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

レシピ内容版

定義元: `database/migrations/002_relational_schema.sql:statement-186`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| recipe_id | uuid | 不可 | なし | なし | 所属レシピ |
| version | integer | 不可 | なし | version &gt; 0 | 版番号 |
| release_id | uuid | 不可 | なし | なし | 採用カタログ版 |
| base_servings | numeric(20,6) | 不可 | なし | base_servings &gt; 0; base_servings IS NULL OR base_servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 登録分量が何人前か |
| output_amount | numeric(20,6) | 不可 | なし | output_amount &gt; 0; output_amount IS NULL OR output_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 完成量 |
| output_unit_id | uuid | 不可 | なし | なし | 完成量単位 |
| status | text | 不可 | なし | status &lt;&gt; 'published' OR (validation = 'passed' AND published_at IS NOT NULL); LENGTH(BTRIM(status)) BETWEEN 1 AND 20000; status IN ('draft', 'published', 'withdrawn') | 版の状態 |
| validation | text | 不可 | なし | status &lt;&gt; 'published' OR (validation = 'passed' AND published_at IS NOT NULL); LENGTH(BTRIM(validation)) BETWEEN 1 AND 20000; validation IN ('pending', 'passed', 'failed', 'needs_review') | 公開審査 |
| content_hash | char(64) | 不可 | なし | content_hash IS NULL OR content_hash ~ '^[0-9a-f]{64}$' | 内容ハッシュ |
| published_at | timestamptz | 可 | なし | status &lt;&gt; 'published' OR (validation = 'passed' AND published_at IS NOT NULL) | 公開日時 |
| description | text | 可 | なし | CHAR_LENGTH(description) &lt;= 5000 | 料理の紹介文 |

## 表制約

- `CHECK (version > 0)`
- `CHECK (base_servings > 0)`
- `CHECK (output_amount > 0)`
- `CHECK (status <> 'published' OR (validation = 'passed' AND published_at IS NOT NULL))`
- `CHECK (base_servings IS NULL OR base_servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (output_amount IS NULL OR output_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000)`
- `CHECK (status IN ('draft', 'published', 'withdrawn'))`
- `CHECK (LENGTH(BTRIM(validation)) BETWEEN 1 AND 20000)`
- `CHECK (validation IN ('pending', 'passed', 'failed', 'needs_review'))`
- `CHECK (content_hash IS NULL OR content_hash ~ '^[0-9a-f]{64}$')`
- `CHECK (CHAR_LENGTH(description) <= 5000)`
- `UNIQUE (recipe_id, version)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_recipe_version_recipe_id | False | (recipe_id) |
| ix_recipe_version_release_id | False | (release_id) |
| ix_recipe_version_output_unit_id | False | (output_unit_id) |
| ix_recipe_version_search_0 | False | ( recipe_id, version DESC ) WHERE status = 'published' |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_recipe_version_recipe_id | recipe_id | recipe(id) | RESTRICT | RESTRICT | True |
| fk_recipe_version_release_id | release_id | catalog_release(id) | RESTRICT | RESTRICT | True |
| fk_recipe_version_output_unit_id | output_unit_id | unit(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / レシピ

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q300_reference_recipe_version.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q300_reference_recipe_version.sql |
| entity_menu_item_create | R | backend/src/app/apis/entities/menu_item_create/sql/003_reference_recipe_version_id.sql |
| entity_menu_item_update | R | backend/src/app/apis/entities/menu_item_update/sql/003_reference_recipe_version_id.sql |
| entity_recipe_version_create | C | backend/src/app/apis/entities/recipe_version_create/sql/001_create.sql |
| entity_recipe_version_get | R | backend/src/app/apis/entities/recipe_version_get/sql/001_get.sql |
| entity_recipe_version_list | R | backend/src/app/apis/entities/recipe_version_list/sql/001_list.sql |
| entity_recipe_version_update | U | backend/src/app/apis/entities/recipe_version_update/sql/001_update.sql |
| entity_user_recipe_event_create | R | backend/src/app/apis/entities/user_recipe_event_create/sql/003_reference_recipe_version_id.sql |
| get_recipe | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| list_recipes | R | backend/src/app/apis/recipes/list_recipes/sql/001_select_recipes.sql |
| random_recipe | R | backend/src/app/apis/recipes/random_recipe/sql/001_random_recipe.sql |
| add_menu_item | R | backend/src/app/apis/workspace/add_menu_item/sql/q010_recipe.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q010_recipe.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q020_steps.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q024_ingredients.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| preview_cooking_plan | R | backend/src/app/apis/workspace/preview_cooking_plan/sql/q001_steps.sql |
| save_recipe | R | backend/src/app/apis/workspace/save_recipe/sql/q001_recipe.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/unsave_recipe/sql/q001_recipe.sql |
| update_menu_item | R | backend/src/app/apis/workspace/update_menu_item/sql/q010_recipe.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| preview_cooking_plan | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
