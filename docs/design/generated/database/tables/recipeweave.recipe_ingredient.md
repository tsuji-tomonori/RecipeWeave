# テーブル仕様: recipeweave.recipe_ingredient

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

レシピ材料明細

定義元: `database/migrations/002_relational_schema.sql:statement-225`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY; kit_parent_line_id IS NULL OR kit_parent_line_id &lt;&gt; id | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| recipe_version_id | uuid | 不可 | なし | なし | 親版 |
| line_no | integer | 不可 | なし | line_no &gt; 0 | 表示順 |
| form_id | uuid | 不可 | なし | なし | 使用形態 |
| product_version_id | uuid | 可 | なし | なし | 商品指定時の仕様版 |
| component_id | uuid | 可 | なし | ( demand_kind = 'kit_component' AND component_id IS NOT NULL AND kit_parent_line_id IS NOT NULL ) OR (demand_kind &lt;&gt; 'kit_component' AND component_id IS NULL AND kit_parent_line_id IS NULL) | セット内構成品を使う場合 |
| kit_parent_line_id | uuid | 可 | なし | ( demand_kind = 'kit_component' AND component_id IS NOT NULL AND kit_parent_line_id IS NOT NULL ) OR (demand_kind &lt;&gt; 'kit_component' AND component_id IS NULL AND kit_parent_line_id IS NULL); kit_parent_line_id IS NULL OR kit_parent_line_id &lt;&gt; id | 購入対象となるセットの親行 |
| role | text | 不可 | なし | LENGTH(BTRIM(role)) BETWEEN 1 AND 20000; role IN ('main', 'support', 'seasoning', 'aroma', 'texture', 'garnish', 'medium') | 料理での役割 |
| demand_kind | text | 不可 | なし | ( demand_kind = 'kit_component' AND component_id IS NOT NULL AND kit_parent_line_id IS NOT NULL ) OR (demand_kind &lt;&gt; 'kit_component' AND component_id IS NULL AND kit_parent_line_id IS NULL); LENGTH(BTRIM(demand_kind)) BETWEEN 1 AND 20000; demand_kind IN ('purchase', 'utility', 'kit_component') | 購入対象区分 |
| amount_mode | text | 不可 | なし | ( amount_mode = 'exact' AND amount IS NOT NULL AND canonical_amount IS NOT NULL AND amount_max IS NULL ) OR ( amount_mode = 'range' AND amount IS NOT NULL AND amount_max IS NOT NULL AND amount_max &gt;= amount AND canonical_amount IS NULL ) OR ( amount_mode = 'to_taste' AND amount IS NULL AND amount_max IS NULL AND canonical_amount IS NULL ); LENGTH(BTRIM(amount_mode)) BETWEEN 1 AND 20000; amount_mode IN ('exact', 'range', 'to_taste') | 確定/範囲/適量 |
| amount | numeric(20,6) | 可 | なし | amount IS NULL OR amount &gt; 0; ( amount_mode = 'exact' AND amount IS NOT NULL AND canonical_amount IS NOT NULL AND amount_max IS NULL ) OR ( amount_mode = 'range' AND amount IS NOT NULL AND amount_max IS NOT NULL AND amount_max &gt;= amount AND canonical_amount IS NULL ) OR ( amount_mode = 'to_taste' AND amount IS NULL AND amount_max IS NULL AND canonical_amount IS NULL ); amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 確定値または範囲下限 |
| amount_max | numeric(20,6) | 可 | なし | amount_max IS NULL OR amount_max &gt; 0; ( amount_mode = 'exact' AND amount IS NOT NULL AND canonical_amount IS NOT NULL AND amount_max IS NULL ) OR ( amount_mode = 'range' AND amount IS NOT NULL AND amount_max IS NOT NULL AND amount_max &gt;= amount AND canonical_amount IS NULL ) OR ( amount_mode = 'to_taste' AND amount IS NULL AND amount_max IS NULL AND canonical_amount IS NULL ); amount_max IS NULL OR amount_max::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 範囲上限 |
| unit_id | uuid | 不可 | なし | なし | 登録単位 |
| canonical_amount | numeric(20,6) | 可 | なし | canonical_amount IS NULL OR canonical_amount &gt; 0; ( amount_mode = 'exact' AND amount IS NOT NULL AND canonical_amount IS NOT NULL AND amount_max IS NULL ) OR ( amount_mode = 'range' AND amount IS NOT NULL AND amount_max IS NOT NULL AND amount_max &gt;= amount AND canonical_amount IS NULL ) OR ( amount_mode = 'to_taste' AND amount IS NULL AND amount_max IS NULL AND canonical_amount IS NULL ); canonical_amount IS NULL OR canonical_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 登録版の基準量 |
| conversion_id | uuid | 可 | なし | なし | 非基準単位の換算根拠 |
| scaling_rule_id | uuid | 不可 | なし | なし | 人数変換規則 |
| optional | boolean | 不可 | なし | なし | 任意追加材料 |
| note | text | 可 | なし | CHAR_LENGTH(note) &lt;= 500 | 材料の補足 |

## 表制約

- `CHECK (line_no > 0)`
- `CHECK (amount IS NULL OR amount > 0)`
- `CHECK (amount_max IS NULL OR amount_max > 0)`
- `CHECK (canonical_amount IS NULL OR canonical_amount > 0)`
- `CHECK (( amount_mode = 'exact' AND amount IS NOT NULL AND canonical_amount IS NOT NULL AND amount_max IS NULL ) OR ( amount_mode = 'range' AND amount IS NOT NULL AND amount_max IS NOT NULL AND amount_max >= amount AND canonical_amount IS NULL ) OR ( amount_mode = 'to_taste' AND amount IS NULL AND amount_max IS NULL AND canonical_amount IS NULL ))`
- `CHECK (( demand_kind = 'kit_component' AND component_id IS NOT NULL AND kit_parent_line_id IS NOT NULL ) OR (demand_kind <> 'kit_component' AND component_id IS NULL AND kit_parent_line_id IS NULL))`
- `CHECK (kit_parent_line_id IS NULL OR kit_parent_line_id <> id)`
- `CHECK (LENGTH(BTRIM(role)) BETWEEN 1 AND 20000)`
- `CHECK (role IN ('main', 'support', 'seasoning', 'aroma', 'texture', 'garnish', 'medium'))`
- `CHECK (LENGTH(BTRIM(demand_kind)) BETWEEN 1 AND 20000)`
- `CHECK (demand_kind IN ('purchase', 'utility', 'kit_component'))`
- `CHECK (LENGTH(BTRIM(amount_mode)) BETWEEN 1 AND 20000)`
- `CHECK (amount_mode IN ('exact', 'range', 'to_taste'))`
- `CHECK (amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (amount_max IS NULL OR amount_max::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (canonical_amount IS NULL OR canonical_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (CHAR_LENGTH(note) <= 500)`
- `UNIQUE (recipe_version_id, line_no)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_recipe_ingredient_recipe_version_id | False | ( recipe_version_id ) |
| ix_recipe_ingredient_form_id | False | (form_id) |
| ix_recipe_ingredient_product_version_id | False | ( product_version_id ) |
| ix_recipe_ingredient_component_id | False | (component_id) |
| ix_recipe_ingredient_kit_parent_line_id | False | ( kit_parent_line_id ) |
| ix_recipe_ingredient_unit_id | False | (unit_id) |
| ix_recipe_ingredient_conversion_id | False | (conversion_id) |
| ix_recipe_ingredient_scaling_rule_id | False | ( scaling_rule_id ) |
| ix_recipe_ingredient_search_0 | False | ( form_id, recipe_version_id ) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_recipe_ingredient_recipe_version_id | recipe_version_id | recipe_version(id) | RESTRICT | RESTRICT | True |
| fk_recipe_ingredient_form_id | form_id | food_form(id) | RESTRICT | RESTRICT | True |
| fk_recipe_ingredient_product_version_id | product_version_id | product_version(id) | RESTRICT | RESTRICT | True |
| fk_recipe_ingredient_component_id | component_id | product_component(id) | RESTRICT | RESTRICT | True |
| fk_recipe_ingredient_kit_parent_line_id | kit_parent_line_id | recipe_ingredient(id) | RESTRICT | RESTRICT | True |
| fk_recipe_ingredient_unit_id | unit_id | unit(id) | RESTRICT | RESTRICT | True |
| fk_recipe_ingredient_conversion_id | conversion_id | conversion(id) | RESTRICT | RESTRICT | True |
| fk_recipe_ingredient_scaling_rule_id | scaling_rule_id | scaling_rule(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / レシピ

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_recipe_ingredient_create | C | backend/src/app/apis/entities/recipe_ingredient_create/sql/001_create.sql |
| entity_recipe_ingredient_get | R | backend/src/app/apis/entities/recipe_ingredient_get/sql/001_get.sql |
| entity_recipe_ingredient_list | R | backend/src/app/apis/entities/recipe_ingredient_list/sql/001_list.sql |
| entity_recipe_ingredient_update | U | backend/src/app/apis/entities/recipe_ingredient_update/sql/001_update.sql |
| get_recipe | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| list_recipes | R | backend/src/app/apis/recipes/list_recipes/sql/001_select_recipes.sql |
| random_recipe | R | backend/src/app/apis/recipes/random_recipe/sql/001_random_recipe.sql |
| add_menu_item | R | backend/src/app/apis/workspace/add_menu_item/sql/q011_ingredients.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q011_ingredients.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q024_ingredients.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_menu_item | R | backend/src/app/apis/workspace/update_menu_item/sql/q011_ingredients.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| preview_cooking_plan | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql |
