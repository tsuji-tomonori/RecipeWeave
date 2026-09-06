# テーブル仕様: recipeweave.unit

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

単位

定義元: `database/migrations/002_relational_schema.sql:statement-20`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| code | text | 不可 | なし | LENGTH(BTRIM(code)) BETWEEN 1 AND 20000 | 単位コード |
| name | text | 不可 | なし | LENGTH(BTRIM(name)) BETWEEN 1 AND 20000 | 表示名 |
| dimension | text | 不可 | なし | LENGTH(BTRIM(dimension)) BETWEEN 1 AND 20000; dimension IN ('mass', 'volume', 'count', 'time', 'temperature', 'length', 'power') | 物理次元 |
| factor | numeric(20,6) | 不可 | なし | factor &gt; 0; factor IS NULL OR factor::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 同一次元の基準単位への倍率 |
| offset | numeric(20,6) | 不可 | なし | "offset" IS NULL OR "offset"::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 温度等のオフセット |
| status | text | 不可 | なし | LENGTH(BTRIM(status)) BETWEEN 1 AND 20000; status IN ('active', 'retired') | 利用状態 |

## 表制約

- `CHECK (factor > 0)`
- `CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(dimension)) BETWEEN 1 AND 20000)`
- `CHECK (dimension IN ('mass', 'volume', 'count', 'time', 'temperature', 'length', 'power'))`
- `CHECK (factor IS NULL OR factor::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK ("offset" IS NULL OR "offset"::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000)`
- `CHECK (status IN ('active', 'retired'))`
- `UNIQUE (code)`
- `PRIMARY KEY (id)`

## 索引

独立索引なし。主キー・一意制約の索引は表制約を参照。

## 外部キー

外部キーなし。

保持・所属領域: catalog / 数量

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q300_reference_unit.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q300_reference_unit.sql |
| entity_unit_create | C | backend/src/app/apis/entities/unit_create/sql/001_create.sql |
| entity_unit_get | R | backend/src/app/apis/entities/unit_get/sql/001_get.sql |
| entity_unit_list | R | backend/src/app/apis/entities/unit_list/sql/001_list.sql |
| entity_unit_update | U | backend/src/app/apis/entities/unit_update/sql/001_update.sql |
| list_foods | R | backend/src/app/apis/foods/list_foods/sql/001_select_foods.sql |
| get_recipe | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| list_recipes | R | backend/src/app/apis/recipes/list_recipes/sql/001_select_recipes.sql |
| random_recipe | R | backend/src/app/apis/recipes/random_recipe/sql/001_random_recipe.sql |
| add_menu_item | R | backend/src/app/apis/workspace/add_menu_item/sql/q011_ingredients.sql |
| commit_receipt | R | backend/src/app/apis/workspace/commit_receipt/sql/q001_resolve_form.sql |
| commit_receipt | R | backend/src/app/apis/workspace/commit_receipt/sql/q022_custom_form.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q011_ingredients.sql |
| create_custom_food | R | backend/src/app/apis/workspace/create_custom_food/sql/q022_custom_form.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/create_pantry_lot/sql/q001_resolve_form.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/put_shopping_checks/sql/q002_insert.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/update_cooking_session/sql/q006_totals.sql |
| update_menu_item | R | backend/src/app/apis/workspace/update_menu_item/sql/q011_ingredients.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/update_pantry_lot/sql/q001_resolve_form.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| preview_cooking_plan | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
