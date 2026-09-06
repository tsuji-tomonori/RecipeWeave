# テーブル仕様: recipeweave.food_form

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

食材形態

定義元: `database/migrations/002_relational_schema.sql:statement-47`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| food_id | uuid | 不可 | なし | なし | 対応食材 |
| name | text | 不可 | なし | LENGTH(BTRIM(name)) BETWEEN 1 AND 20000; CHAR_LENGTH(name) &lt;= 500 | 生皮付き・冷凍刻み等 |
| state | text | 不可 | なし | LENGTH(BTRIM(state)) BETWEEN 1 AND 20000; state IN ('raw', 'dry', 'frozen', 'cooked', 'rehydrated', 'drained', 'peeled', 'ready') | 処理状態 |
| base_unit_id | uuid | 不可 | なし | なし | 計算基準単位 |
| quantity_basis | text | 不可 | なし | LENGTH(BTRIM(quantity_basis)) BETWEEN 1 AND 20000; quantity_basis IN ('edible', 'as_purchased', 'drained', 'prepared') | 数量の対象部分 |
| status | text | 不可 | なし | LENGTH(BTRIM(status)) BETWEEN 1 AND 20000; status IN ('active', 'retired') | 利用状態 |

## 表制約

- `CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(state)) BETWEEN 1 AND 20000)`
- `CHECK (state IN ('raw', 'dry', 'frozen', 'cooked', 'rehydrated', 'drained', 'peeled', 'ready'))`
- `CHECK (LENGTH(BTRIM(quantity_basis)) BETWEEN 1 AND 20000)`
- `CHECK (quantity_basis IN ('edible', 'as_purchased', 'drained', 'prepared'))`
- `CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000)`
- `CHECK (status IN ('active', 'retired'))`
- `CHECK (CHAR_LENGTH(name) <= 500)`
- `UNIQUE (food_id, name)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_food_form_food_id | False | (food_id) |
| ix_food_form_base_unit_id | False | (base_unit_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_food_form_food_id | food_id | food(id) | RESTRICT | RESTRICT | True |
| fk_food_form_base_unit_id | base_unit_id | unit(id) | RESTRICT | RESTRICT | True |

保持・所属領域: catalog / 食材

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| export_backup | R | backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q100_delete_conversion.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q100_delete_food_allergen.sql |
| preview_backup | D | backend/src/app/apis/backup/preview_backup/sql/q100_delete_food_form.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q100_delete_form_yield.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q100_delete_nutrition_fact.sql |
| preview_backup | C | backend/src/app/apis/backup/preview_backup/sql/q200_insert_food_form.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q300_reference_food_form.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q010_export_tables.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q100_delete_conversion.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q100_delete_food_allergen.sql |
| restore_backup | D | backend/src/app/apis/backup/restore_backup/sql/q100_delete_food_form.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q100_delete_form_yield.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q100_delete_nutrition_fact.sql |
| restore_backup | C | backend/src/app/apis/backup/restore_backup/sql/q200_insert_food_form.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q300_reference_food_form.sql |
| entity_food_form_create | C | backend/src/app/apis/entities/food_form_create/sql/001_create.sql |
| entity_food_form_get | R | backend/src/app/apis/entities/food_form_get/sql/001_get.sql |
| entity_food_form_list | R | backend/src/app/apis/entities/food_form_list/sql/001_list.sql |
| entity_food_form_update | U | backend/src/app/apis/entities/food_form_update/sql/001_update.sql |
| list_foods | R | backend/src/app/apis/foods/list_foods/sql/001_select_foods.sql |
| get_recipe | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| list_recipes | R | backend/src/app/apis/recipes/list_recipes/sql/001_select_recipes.sql |
| random_recipe | R | backend/src/app/apis/recipes/random_recipe/sql/001_random_recipe.sql |
| add_menu_item | R | backend/src/app/apis/workspace/add_menu_item/sql/q011_ingredients.sql |
| commit_receipt | R | backend/src/app/apis/workspace/commit_receipt/sql/q001_resolve_form.sql |
| commit_receipt | C | backend/src/app/apis/workspace/commit_receipt/sql/q022_custom_form.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q011_ingredients.sql |
| create_custom_food | C | backend/src/app/apis/workspace/create_custom_food/sql/q022_custom_form.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/create_pantry_lot/sql/q001_resolve_form.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/update_cooking_session/sql/q006_totals.sql |
| update_menu_item | R | backend/src/app/apis/workspace/update_menu_item/sql/q011_ingredients.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/update_pantry_lot/sql/q001_resolve_form.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| preview_cooking_plan | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
