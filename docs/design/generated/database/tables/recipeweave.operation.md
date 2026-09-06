# テーブル仕様: recipeweave.operation

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

標準調理動作

定義元: `database/migrations/002_relational_schema.sql:statement-245`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| code | text | 不可 | なし | LENGTH(BTRIM(code)) BETWEEN 1 AND 20000 | cut_ginkgo等 |
| name | text | 不可 | なし | LENGTH(BTRIM(name)) BETWEEN 1 AND 20000 | いちょう切り等 |
| definition | text | 不可 | なし | LENGTH(BTRIM(definition)) BETWEEN 1 AND 20000 | 動作の意味 |
| precondition | text | 不可 | なし | LENGTH(BTRIM(precondition)) BETWEEN 1 AND 20000 | 入力食材・必要状態 |
| completion_cue | text | 不可 | なし | LENGTH(BTRIM(completion_cue)) BETWEEN 1 AND 20000 | 完了確認方法 |
| status | text | 不可 | なし | LENGTH(BTRIM(status)) BETWEEN 1 AND 20000; status IN ('active', 'retired') | 使用状態 |

## 表制約

- `CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(definition)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(precondition)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(completion_cue)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000)`
- `CHECK (status IN ('active', 'retired'))`
- `UNIQUE (code)`
- `PRIMARY KEY (id)`

## 索引

独立索引なし。主キー・一意制約の索引は表制約を参照。

## 外部キー

外部キーなし。

保持・所属領域: catalog / 工程

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_operation_create | C | backend/src/app/apis/entities/operation_create/sql/001_create.sql |
| entity_operation_get | R | backend/src/app/apis/entities/operation_get/sql/001_get.sql |
| entity_operation_list | R | backend/src/app/apis/entities/operation_list/sql/001_list.sql |
| entity_operation_update | U | backend/src/app/apis/entities/operation_update/sql/001_update.sql |
| get_recipe | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| list_recipes | R | backend/src/app/apis/recipes/list_recipes/sql/001_select_recipes.sql |
| random_recipe | R | backend/src/app/apis/recipes/random_recipe/sql/001_random_recipe.sql |
| preview_cooking_plan | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
