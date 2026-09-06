# テーブル仕様: recipeweave.scaling_rule

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

人数変更規則

定義元: `database/migrations/002_relational_schema.sql:statement-206`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| name | text | 不可 | なし | LENGTH(BTRIM(name)) BETWEEN 1 AND 20000 | 規則名 |
| mode | text | 不可 | なし | mode NOT IN ('fixed_batch', 'capacity_batch') OR batch_capacity IS NOT NULL; LENGTH(BTRIM(mode)) BETWEEN 1 AND 20000; mode IN ('linear', 'fixed_batch', 'capacity_batch', 'validated_curve', 'manual') | 比例・バッチ等 |
| min_servings | numeric(20,6) | 不可 | なし | min_servings &gt; 0; max_servings &gt;= min_servings; min_servings IS NULL OR min_servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 検証済み人数下限 |
| max_servings | numeric(20,6) | 不可 | なし | max_servings &gt;= min_servings; max_servings IS NULL OR max_servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 検証済み人数上限 |
| batch_capacity | numeric(20,6) | 可 | なし | batch_capacity IS NULL OR batch_capacity &gt; 0; mode NOT IN ('fixed_batch', 'capacity_batch') OR batch_capacity IS NOT NULL; batch_capacity IS NULL OR batch_capacity::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 1バッチ上限 |
| round_mode | text | 不可 | なし | LENGTH(BTRIM(round_mode)) BETWEEN 1 AND 20000; round_mode IN ('none', 'half_up', 'ceil') | 表示丸め |
| round_increment | numeric(20,6) | 不可 | なし | round_increment &gt; 0; round_increment IS NULL OR round_increment::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 表示・購入の刻み |
| source_id | uuid | 可 | なし | なし | 検証根拠 |

## 表制約

- `CHECK (min_servings > 0)`
- `CHECK (max_servings >= min_servings)`
- `CHECK (round_increment > 0)`
- `CHECK (batch_capacity IS NULL OR batch_capacity > 0)`
- `CHECK (mode NOT IN ('fixed_batch', 'capacity_batch') OR batch_capacity IS NOT NULL)`
- `CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(mode)) BETWEEN 1 AND 20000)`
- `CHECK (mode IN ('linear', 'fixed_batch', 'capacity_batch', 'validated_curve', 'manual'))`
- `CHECK (min_servings IS NULL OR min_servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (max_servings IS NULL OR max_servings::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (batch_capacity IS NULL OR batch_capacity::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (LENGTH(BTRIM(round_mode)) BETWEEN 1 AND 20000)`
- `CHECK (round_mode IN ('none', 'half_up', 'ceil'))`
- `CHECK (round_increment IS NULL OR round_increment::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_scaling_rule_source_id | False | (source_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_scaling_rule_source_id | source_id | source_record(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 数量

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_scaling_rule_create | C | backend/src/app/apis/entities/scaling_rule_create/sql/001_create.sql |
| entity_scaling_rule_get | R | backend/src/app/apis/entities/scaling_rule_get/sql/001_get.sql |
| entity_scaling_rule_list | R | backend/src/app/apis/entities/scaling_rule_list/sql/001_list.sql |
| get_recipe | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| list_recipes | R | backend/src/app/apis/recipes/list_recipes/sql/001_select_recipes.sql |
| random_recipe | R | backend/src/app/apis/recipes/random_recipe/sql/001_random_recipe.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q020_steps.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| preview_cooking_plan | R | backend/src/app/apis/workspace/preview_cooking_plan/sql/q001_steps.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| preview_cooking_plan | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
