# テーブル仕様: recipeweave.operation_parameter

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

動作パラメータ定義

定義元: `database/migrations/002_relational_schema.sql:statement-255`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| operation_id | uuid | 不可 | なし | なし | 動作 |
| code | text | 不可 | なし | LENGTH(BTRIM(code)) BETWEEN 1 AND 20000 | thickness_mm等 |
| name | text | 不可 | なし | LENGTH(BTRIM(name)) BETWEEN 1 AND 20000 | 厚さ等 |
| value_type | text | 不可 | なし | ( value_type = 'option' AND allowed_values IS NOT NULL AND JSONB_TYPEOF(allowed_values) = 'array' AND JSONB_ARRAY_LENGTH(allowed_values) BETWEEN 1 AND 100 ) OR (value_type &lt;&gt; 'option' AND allowed_values IS NULL); LENGTH(BTRIM(value_type)) BETWEEN 1 AND 20000; value_type IN ('decimal', 'integer', 'boolean', 'text', 'option') | 値型 |
| unit_id | uuid | 可 | なし | なし | 単位 |
| required | boolean | 不可 | なし | なし | 必須か |
| min_value | numeric(20,6) | 可 | なし | min_value IS NULL OR max_value IS NULL OR min_value &lt;= max_value; min_value IS NULL OR min_value::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 許容下限 |
| max_value | numeric(20,6) | 可 | なし | min_value IS NULL OR max_value IS NULL OR min_value &lt;= max_value; max_value IS NULL OR max_value::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 許容上限 |
| allowed_values | jsonb | 可 | なし | ( value_type = 'option' AND allowed_values IS NOT NULL AND JSONB_TYPEOF(allowed_values) = 'array' AND JSONB_ARRAY_LENGTH(allowed_values) BETWEEN 1 AND 100 ) OR (value_type &lt;&gt; 'option' AND allowed_values IS NULL); allowed_values IS NULL OR PG_COLUMN_SIZE(allowed_values) &lt;= 1048576 | option型の具体値配列 |

## 表制約

- `CHECK (min_value IS NULL OR max_value IS NULL OR min_value <= max_value)`
- `CHECK (( value_type = 'option' AND allowed_values IS NOT NULL AND JSONB_TYPEOF(allowed_values) = 'array' AND JSONB_ARRAY_LENGTH(allowed_values) BETWEEN 1 AND 100 ) OR (value_type <> 'option' AND allowed_values IS NULL))`
- `CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(value_type)) BETWEEN 1 AND 20000)`
- `CHECK (value_type IN ('decimal', 'integer', 'boolean', 'text', 'option'))`
- `CHECK (min_value IS NULL OR min_value::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (max_value IS NULL OR max_value::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (allowed_values IS NULL OR PG_COLUMN_SIZE(allowed_values) <= 1048576)`
- `UNIQUE (operation_id, code)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_operation_parameter_operation_id | False | (operation_id) |
| ix_operation_parameter_unit_id | False | (unit_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_operation_parameter_operation_id | operation_id | operation(id) | RESTRICT | RESTRICT | True |
| fk_operation_parameter_unit_id | unit_id | unit(id) | RESTRICT | RESTRICT | True |

保持・所属領域: catalog / 工程

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_operation_parameter_create | C | backend/src/app/apis/entities/operation_parameter_create/sql/001_create.sql |
| entity_operation_parameter_get | R | backend/src/app/apis/entities/operation_parameter_get/sql/001_get.sql |
| entity_operation_parameter_list | R | backend/src/app/apis/entities/operation_parameter_list/sql/001_list.sql |
| entity_operation_parameter_update | U | backend/src/app/apis/entities/operation_parameter_update/sql/001_update.sql |
