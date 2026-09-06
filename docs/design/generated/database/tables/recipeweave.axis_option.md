# テーブル仕様: recipeweave.axis_option

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

軸候補値

定義元: `database/migrations/002_relational_schema.sql:statement-162`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| axis_id | uuid | 不可 | なし | なし | 親軸 |
| code | text | 不可 | なし | LENGTH(BTRIM(code)) BETWEEN 1 AND 20000 | 値コード |
| label | text | 不可 | なし | LENGTH(BTRIM(label)) BETWEEN 1 AND 20000; CHAR_LENGTH(label) &lt;= 500 | 候補名 |
| definition | text | 不可 | なし | LENGTH(BTRIM(definition)) BETWEEN 1 AND 20000 | 値の意味 |
| parent_id | uuid | 可 | なし | なし | 同軸の階層親 |
| status | text | 不可 | なし | LENGTH(BTRIM(status)) BETWEEN 1 AND 20000; status IN ('active', 'retired') | 選択可否 |

## 表制約

- `CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(label)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(definition)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000)`
- `CHECK (status IN ('active', 'retired'))`
- `CHECK (CHAR_LENGTH(label) <= 500)`
- `UNIQUE (axis_id, code)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_axis_option_axis_id | False | (axis_id) |
| ix_axis_option_parent_id | False | (parent_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_axis_option_axis_id | axis_id | axis(id) | RESTRICT | RESTRICT | True |
| fk_axis_option_parent_id | parent_id | axis_option(id) | RESTRICT | RESTRICT | True |

保持・所属領域: catalog / 発想

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q300_reference_axis_option.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q300_reference_axis_option.sql |
| entity_axis_option_create | C | backend/src/app/apis/entities/axis_option_create/sql/001_create.sql |
| entity_axis_option_get | R | backend/src/app/apis/entities/axis_option_get/sql/001_get.sql |
| entity_axis_option_list | R | backend/src/app/apis/entities/axis_option_list/sql/001_list.sql |
| entity_axis_option_update | U | backend/src/app/apis/entities/axis_option_update/sql/001_update.sql |
| list_foods | R | backend/src/app/apis/foods/list_foods/sql/001_select_foods.sql |
| get_recipe | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| list_recipes | R | backend/src/app/apis/recipes/list_recipes/sql/001_select_recipes.sql |
| random_recipe | R | backend/src/app/apis/recipes/random_recipe/sql/001_random_recipe.sql |
| add_menu_item | R | backend/src/app/apis/workspace/add_menu_item/sql/q010_recipe.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q010_recipe.sql |
| update_menu_item | R | backend/src/app/apis/workspace/update_menu_item/sql/q010_recipe.sql |
| preview_cooking_plan | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
