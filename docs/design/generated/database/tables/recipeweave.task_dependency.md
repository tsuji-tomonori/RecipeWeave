# テーブル仕様: recipeweave.task_dependency

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

献立展開後依存

定義元: `database/migrations/002_relational_schema.sql:statement-531`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| before_task_id | uuid | 不可 | なし | before_task_id &lt;&gt; after_task_id | 先行タスク |
| after_task_id | uuid | 不可 | なし | before_task_id &lt;&gt; after_task_id | 後続タスク |
| min_lag_s | integer | 不可 | なし | min_lag_s &gt;= 0; max_lag_s IS NULL OR max_lag_s &gt;= min_lag_s | 最小間隔 |
| max_lag_s | integer | 可 | なし | max_lag_s IS NULL OR max_lag_s &gt;= min_lag_s | 最大間隔 |
| reason | text | 不可 | なし | LENGTH(BTRIM(reason)) BETWEEN 1 AND 20000 | 元DAG/洗浄/設備切替等 |

## 表制約

- `CHECK (before_task_id <> after_task_id)`
- `CHECK (min_lag_s >= 0)`
- `CHECK (max_lag_s IS NULL OR max_lag_s >= min_lag_s)`
- `CHECK (LENGTH(BTRIM(reason)) BETWEEN 1 AND 20000)`
- `UNIQUE (before_task_id, after_task_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_task_dependency_before_task_id | False | (before_task_id) |
| ix_task_dependency_after_task_id | False | (after_task_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_task_dependency_before_task_id | before_task_id | session_task(id) | CASCADE | RESTRICT | True |
| fk_task_dependency_after_task_id | after_task_id | session_task(id) | CASCADE | RESTRICT | True |

保持・所属領域: owned / 献立

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_task_dependency_create | C | backend/src/app/apis/entities/task_dependency_create/sql/001_create.sql |
| entity_task_dependency_delete | D | backend/src/app/apis/entities/task_dependency_delete/sql/001_delete.sql |
| entity_task_dependency_get | R | backend/src/app/apis/entities/task_dependency_get/sql/001_get.sql |
| entity_task_dependency_list | R | backend/src/app/apis/entities/task_dependency_list/sql/001_list.sql |
| entity_task_dependency_update | U | backend/src/app/apis/entities/task_dependency_update/sql/001_update.sql |
| create_cooking_session | C | backend/src/app/apis/workspace/create_cooking_session/sql/q027_dependency.sql |
