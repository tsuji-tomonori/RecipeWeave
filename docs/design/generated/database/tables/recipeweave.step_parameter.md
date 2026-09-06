# テーブル仕様: recipeweave.step_parameter

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

工程の型付きパラメータ

定義元: `database/migrations/002_relational_schema.sql:statement-281`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| step_id | uuid | 不可 | なし | なし | 対象工程 |
| parameter_id | uuid | 不可 | なし | なし | 動作パラメータ |
| number_value | numeric(20,6) | 可 | なし | NUM_NONNULLS(number_value, text_value, bool_value) = 1; number_value IS NULL OR number_value::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 数値 |
| text_value | text | 可 | なし | NUM_NONNULLS(number_value, text_value, bool_value) = 1 | 文字・optionコード |
| bool_value | boolean | 可 | なし | NUM_NONNULLS(number_value, text_value, bool_value) = 1 | 真偽 |

## 表制約

- `CHECK (NUM_NONNULLS(number_value, text_value, bool_value) = 1)`
- `CHECK (number_value IS NULL OR number_value::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `UNIQUE (step_id, parameter_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_step_parameter_step_id | False | (step_id) |
| ix_step_parameter_parameter_id | False | (parameter_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_step_parameter_step_id | step_id | recipe_step(id) | RESTRICT | RESTRICT | True |
| fk_step_parameter_parameter_id | parameter_id | operation_parameter(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 工程

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_step_parameter_create | C | backend/src/app/apis/entities/step_parameter_create/sql/001_create.sql |
| entity_step_parameter_get | R | backend/src/app/apis/entities/step_parameter_get/sql/001_get.sql |
| entity_step_parameter_list | R | backend/src/app/apis/entities/step_parameter_list/sql/001_list.sql |
| entity_step_parameter_update | U | backend/src/app/apis/entities/step_parameter_update/sql/001_update.sql |
