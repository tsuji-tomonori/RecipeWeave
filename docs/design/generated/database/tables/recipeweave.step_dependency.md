# テーブル仕様: recipeweave.step_dependency

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

工程依存辺

定義元: `database/migrations/002_relational_schema.sql:statement-308`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| before_step_id | uuid | 不可 | なし | before_step_id &lt;&gt; after_step_id | 先行工程 |
| after_step_id | uuid | 不可 | なし | before_step_id &lt;&gt; after_step_id | 後続工程 |
| kind | text | 不可 | なし | LENGTH(BTRIM(kind)) BETWEEN 1 AND 20000; kind IN ('material', 'sequence', 'safety', 'quality') | 依存理由 |
| min_lag_s | integer | 不可 | なし | min_lag_s &gt;= 0; max_lag_s IS NULL OR max_lag_s &gt;= min_lag_s | 完了後最低待機 |
| max_lag_s | integer | 可 | なし | max_lag_s IS NULL OR max_lag_s &gt;= min_lag_s | 品質上の最大待機 |

## 表制約

- `CHECK (before_step_id <> after_step_id)`
- `CHECK (min_lag_s >= 0)`
- `CHECK (max_lag_s IS NULL OR max_lag_s >= min_lag_s)`
- `CHECK (LENGTH(BTRIM(kind)) BETWEEN 1 AND 20000)`
- `CHECK (kind IN ('material', 'sequence', 'safety', 'quality'))`
- `UNIQUE (before_step_id, after_step_id, kind)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_step_dependency_before_step_id | False | (before_step_id) |
| ix_step_dependency_after_step_id | False | (after_step_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_step_dependency_before_step_id | before_step_id | recipe_step(id) | RESTRICT | RESTRICT | True |
| fk_step_dependency_after_step_id | after_step_id | recipe_step(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 工程

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_step_dependency_create | C | backend/src/app/apis/entities/step_dependency_create/sql/001_create.sql |
| entity_step_dependency_get | R | backend/src/app/apis/entities/step_dependency_get/sql/001_get.sql |
| entity_step_dependency_list | R | backend/src/app/apis/entities/step_dependency_list/sql/001_list.sql |
| entity_step_dependency_update | U | backend/src/app/apis/entities/step_dependency_update/sql/001_update.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q021_dependencies.sql |
| preview_cooking_plan | R | backend/src/app/apis/workspace/preview_cooking_plan/sql/q002_dependencies.sql |
