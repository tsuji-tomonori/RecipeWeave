# テーブル仕様: recipeweave.menu_ingredient_override

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

献立別材料確定

定義元: `database/migrations/002_relational_schema.sql:statement-488`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| menu_item_id | uuid | 不可 | なし | なし | 対象料理 |
| ingredient_line_id | uuid | 不可 | なし | なし | 元材料行 |
| selected | boolean | 不可 | なし | なし | 任意材料を使うか |
| amount | numeric(20,6) | 可 | なし | amount IS NULL OR amount &gt; 0; amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 適量等の確定基準量 |
| form_id | uuid | 可 | なし | なし | 明示的代替形態 |
| product_version_id | uuid | 可 | なし | なし | 購入商品指定 |

## 表制約

- `CHECK (amount IS NULL OR amount > 0)`
- `CHECK (amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `UNIQUE (menu_item_id, ingredient_line_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_menu_ingredient_override_menu_item_id | False | ( menu_item_id ) |
| ix_menu_ingredient_override_ingredient_line_id | False | ( ingredient_line_id ) |
| ix_menu_ingredient_override_form_id | False | (form_id) |
| ix_menu_ingredient_override_product_version_id | False | ( product_version_id ) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_menu_ingredient_override_menu_item_id | menu_item_id | menu_item(id) | CASCADE | RESTRICT | True |
| fk_menu_ingredient_override_ingredient_line_id | ingredient_line_id | recipe_ingredient(id) | RESTRICT | RESTRICT | True |
| fk_menu_ingredient_override_form_id | form_id | food_form(id) | RESTRICT | RESTRICT | True |
| fk_menu_ingredient_override_product_version_id | product_version_id | product_version(id) | RESTRICT | RESTRICT | True |

保持・所属領域: owned / 献立

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_menu_ingredient_override_create | C | backend/src/app/apis/entities/menu_ingredient_override_create/sql/001_create.sql |
| entity_menu_ingredient_override_delete | D | backend/src/app/apis/entities/menu_ingredient_override_delete/sql/001_delete.sql |
| entity_menu_ingredient_override_get | R | backend/src/app/apis/entities/menu_ingredient_override_get/sql/001_get.sql |
| entity_menu_ingredient_override_list | R | backend/src/app/apis/entities/menu_ingredient_override_list/sql/001_list.sql |
| entity_menu_ingredient_override_update | U | backend/src/app/apis/entities/menu_ingredient_override_update/sql/001_update.sql |
| add_menu_item | C | backend/src/app/apis/workspace/add_menu_item/sql/q014_override.sql |
| create_cooking_session | C | backend/src/app/apis/workspace/create_cooking_session/sql/q014_override.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q024_ingredients.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_menu_item | C | backend/src/app/apis/workspace/update_menu_item/sql/q014_override.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
