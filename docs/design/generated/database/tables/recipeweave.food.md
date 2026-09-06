# テーブル仕様: recipeweave.food

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

購入・利用食材概念

定義元: `database/migrations/002_relational_schema.sql:statement-30`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| code | text | 不可 | なし | LENGTH(BTRIM(code)) BETWEEN 1 AND 20000 | 固定食材コード |
| name | text | 不可 | なし | LENGTH(BTRIM(name)) BETWEEN 1 AND 20000; CHAR_LENGTH(name) &lt;= 100 | 食材名・加工品種別 |
| kind | text | 不可 | なし | LENGTH(BTRIM(kind)) BETWEEN 1 AND 20000; kind IN ('basic', 'processed', 'ready_meal', 'kit', 'utility') | 基本食材か加工食品か |
| parent_id | uuid | 可 | なし | なし | カテゴリ親 |
| release_id | uuid | 不可 | なし | なし | 所属公開版 |
| status | text | 不可 | なし | LENGTH(BTRIM(status)) BETWEEN 1 AND 20000; status IN ('active', 'retired') | 新規使用可否 |
| owner_id | uuid | 可 | なし | なし | 私有食材の所有者。NULLは共通カタログ食材 |

## 表制約

- `CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(kind)) BETWEEN 1 AND 20000)`
- `CHECK (kind IN ('basic', 'processed', 'ready_meal', 'kit', 'utility'))`
- `CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000)`
- `CHECK (status IN ('active', 'retired'))`
- `CHECK (CHAR_LENGTH(name) <= 100)`
- `UNIQUE (code, release_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_food_parent_id | False | (parent_id) |
| ix_food_release_id | False | (release_id) |
| ix_food_owner_id | False | (owner_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_food_parent_id | parent_id | food(id) | RESTRICT | RESTRICT | True |
| fk_food_release_id | release_id | catalog_release(id) | RESTRICT | RESTRICT | True |
| fk_food_owner_id | owner_id | app_user(id) | RESTRICT | RESTRICT | True |

保持・所属領域: catalog / 食材

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_food_create | C | backend/src/app/apis/entities/food_create/sql/001_create.sql |
| entity_food_get | R | backend/src/app/apis/entities/food_get/sql/001_get.sql |
| entity_food_list | R | backend/src/app/apis/entities/food_list/sql/001_list.sql |
| entity_food_update | U | backend/src/app/apis/entities/food_update/sql/001_update.sql |
| list_foods | R | backend/src/app/apis/foods/list_foods/sql/001_select_foods.sql |
| commit_receipt | R | backend/src/app/apis/workspace/commit_receipt/sql/q001_resolve_form.sql |
| commit_receipt | C | backend/src/app/apis/workspace/commit_receipt/sql/q020_custom_food.sql |
| create_custom_food | C | backend/src/app/apis/workspace/create_custom_food/sql/q020_custom_food.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/create_pantry_lot/sql/q001_resolve_form.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/update_pantry_lot/sql/q001_resolve_form.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql |
