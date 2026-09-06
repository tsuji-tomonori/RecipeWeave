# テーブル仕様: recipeweave.validation_result

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

公開前評価結果

定義元: `database/migrations/002_relational_schema.sql:statement-411`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| recipe_version_id | uuid | 不可 | なし | なし | 対象版 |
| rule_id | uuid | 不可 | なし | なし | 適用規則版 |
| state | text | 不可 | なし | LENGTH(BTRIM(state)) BETWEEN 1 AND 20000; state IN ('pending', 'passed', 'failed', 'needs_review') | 結果 |
| evidence | jsonb | 不可 | なし | evidence IS NULL OR PG_COLUMN_SIZE(evidence) &lt;= 1048576 | 検査箇所・値・根拠 |
| validator_version | text | 不可 | なし | LENGTH(BTRIM(validator_version)) BETWEEN 1 AND 20000 | 検証器版 |
| evaluated_at | timestamptz | 不可 | なし | なし | 検査日時 |

## 表制約

- `CHECK (LENGTH(BTRIM(state)) BETWEEN 1 AND 20000)`
- `CHECK (state IN ('pending', 'passed', 'failed', 'needs_review'))`
- `CHECK (evidence IS NULL OR PG_COLUMN_SIZE(evidence) <= 1048576)`
- `CHECK (LENGTH(BTRIM(validator_version)) BETWEEN 1 AND 20000)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_validation_result_recipe_version_id | False | ( recipe_version_id ) |
| ix_validation_result_rule_id | False | (rule_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_validation_result_recipe_version_id | recipe_version_id | recipe_version(id) | RESTRICT | RESTRICT | True |
| fk_validation_result_rule_id | rule_id | compatibility_rule(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 生成

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_validation_result_create | C | backend/src/app/apis/entities/validation_result_create/sql/001_create.sql |
| entity_validation_result_get | R | backend/src/app/apis/entities/validation_result_get/sql/001_get.sql |
| entity_validation_result_list | R | backend/src/app/apis/entities/validation_result_list/sql/001_list.sql |
| get_recipe | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| list_recipes | R | backend/src/app/apis/recipes/list_recipes/sql/001_select_recipes.sql |
| random_recipe | R | backend/src/app/apis/recipes/random_recipe/sql/001_random_recipe.sql |
| preview_cooking_plan | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
