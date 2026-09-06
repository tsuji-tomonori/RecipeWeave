# テーブル仕様: recipeweave.generation_job

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

事前生成ジョブ

定義元: `database/migrations/002_relational_schema.sql:statement-365`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| policy_id | uuid | 不可 | なし | なし | 実行方針 |
| idempotency_key | char(64) | 不可 | なし | idempotency_key IS NULL OR idempotency_key ~ '^[0-9a-f]{64}$' | 入力と方針から作る重複キー |
| status | text | 不可 | なし | LENGTH(BTRIM(status)) BETWEEN 1 AND 20000; status IN ('queued', 'running', 'succeeded', 'failed', 'cancelled') | 進行状態 |
| started_at | timestamptz | 可 | なし | finished_at IS NULL OR (started_at IS NOT NULL AND finished_at &gt;= started_at) | 開始 |
| finished_at | timestamptz | 可 | なし | finished_at IS NULL OR (started_at IS NOT NULL AND finished_at &gt;= started_at) | 終了 |
| seed | integer | 可 | なし | なし | 再現用seed |
| error_code | text | 可 | なし | なし | 失敗分類 |
| attempt_count | integer | 不可 | なし | attempt_count &gt;= 0 | 試行回数 |

## 表制約

- `CHECK (attempt_count >= 0)`
- `CHECK (finished_at IS NULL OR (started_at IS NOT NULL AND finished_at >= started_at))`
- `CHECK (idempotency_key IS NULL OR idempotency_key ~ '^[0-9a-f]{64}$')`
- `CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000)`
- `CHECK (status IN ('queued', 'running', 'succeeded', 'failed', 'cancelled'))`
- `UNIQUE (idempotency_key)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_generation_job_policy_id | False | (policy_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_generation_job_policy_id | policy_id | generation_policy(id) | RESTRICT | RESTRICT | True |

保持・所属領域: transient / 生成

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_generation_job_create | C | backend/src/app/apis/entities/generation_job_create/sql/001_create.sql |
| entity_generation_job_get | R | backend/src/app/apis/entities/generation_job_get/sql/001_get.sql |
| entity_generation_job_list | R | backend/src/app/apis/entities/generation_job_list/sql/001_list.sql |
| entity_generation_job_update | U | backend/src/app/apis/entities/generation_job_update/sql/001_update.sql |
