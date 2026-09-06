# テーブル仕様: recipeweave.step_input

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

工程への材料受渡し

定義元: `database/migrations/002_relational_schema.sql:statement-301`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| step_id | uuid | 不可 | なし | なし | 受取工程 |
| material_id | uuid | 不可 | なし | なし | 受け渡す材料 |
| fraction | numeric(20,6) | 不可 | なし | fraction &gt; 0 AND fraction &lt;= 1; fraction IS NULL OR fraction::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 当該ノード生成量の利用割合 |

## 表制約

- `CHECK (fraction > 0 AND fraction <= 1)`
- `CHECK (fraction IS NULL OR fraction::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `UNIQUE (step_id, material_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_step_input_step_id | False | (step_id) |
| ix_step_input_material_id | False | (material_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_step_input_step_id | step_id | recipe_step(id) | RESTRICT | RESTRICT | True |
| fk_step_input_material_id | material_id | material_node(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 工程

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_step_input_create | C | backend/src/app/apis/entities/step_input_create/sql/001_create.sql |
| entity_step_input_get | R | backend/src/app/apis/entities/step_input_get/sql/001_get.sql |
| entity_step_input_list | R | backend/src/app/apis/entities/step_input_list/sql/001_list.sql |
| entity_step_input_update | U | backend/src/app/apis/entities/step_input_update/sql/001_update.sql |
