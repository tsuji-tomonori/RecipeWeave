# テーブル仕様: recipeweave.food_axis_option

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

食材の分類属性

定義元: `database/migrations/002_relational_schema.sql:statement-172`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| food_id | uuid | 不可 | なし | なし | 食材 |
| option_id | uuid | 不可 | なし | なし | カテゴリ・入手性等の値 |

## 表制約

- `UNIQUE (food_id, option_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_food_axis_option_food_id | False | (food_id) |
| ix_food_axis_option_option_id | False | (option_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_food_axis_option_food_id | food_id | food(id) | RESTRICT | RESTRICT | True |
| fk_food_axis_option_option_id | option_id | axis_option(id) | RESTRICT | RESTRICT | True |

保持・所属領域: catalog / 発想

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_food_axis_option_create | C | backend/src/app/apis/entities/food_axis_option_create/sql/001_create.sql |
| entity_food_axis_option_get | R | backend/src/app/apis/entities/food_axis_option_get/sql/001_get.sql |
| entity_food_axis_option_list | R | backend/src/app/apis/entities/food_axis_option_list/sql/001_list.sql |
| entity_food_axis_option_update | U | backend/src/app/apis/entities/food_axis_option_update/sql/001_update.sql |
| list_foods | R | backend/src/app/apis/foods/list_foods/sql/001_select_foods.sql |
