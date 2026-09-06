# テーブル仕様: recipeweave.generation_result

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

生成結果の出自

定義元: `database/migrations/002_relational_schema.sql:statement-390`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| recipe_version_id | uuid | 不可 | なし | なし | 生成した版 |
| job_id | uuid | 可 | なし | なし | 短期ジョブ参照 |
| policy_id | uuid | 不可 | なし | なし | 恒久方針参照 |
| input_snapshot | jsonb | 不可 | なし | input_snapshot IS NULL OR PG_COLUMN_SIZE(input_snapshot) &lt;= 1048576 | 確定入力をschema_versionで検証 |
| raw_output_uri | text | 可 | なし | なし | 原出力保存先 |
| raw_output_hash | char(64) | 不可 | なし | raw_output_hash IS NULL OR raw_output_hash ~ '^[0-9a-f]{64}$' | 原出力ハッシュ |

## 表制約

- `CHECK (input_snapshot IS NULL OR PG_COLUMN_SIZE(input_snapshot) <= 1048576)`
- `CHECK (raw_output_hash IS NULL OR raw_output_hash ~ '^[0-9a-f]{64}$')`
- `UNIQUE (recipe_version_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_generation_result_recipe_version_id | False | ( recipe_version_id ) |
| ix_generation_result_job_id | False | (job_id) |
| ix_generation_result_policy_id | False | (policy_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_generation_result_recipe_version_id | recipe_version_id | recipe_version(id) | RESTRICT | RESTRICT | True |
| fk_generation_result_job_id | job_id | generation_job(id) | SET NULL | RESTRICT | True |
| fk_generation_result_policy_id | policy_id | generation_policy(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 生成

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_generation_result_create | C | backend/src/app/apis/entities/generation_result_create/sql/001_create.sql |
| entity_generation_result_get | R | backend/src/app/apis/entities/generation_result_get/sql/001_get.sql |
| entity_generation_result_list | R | backend/src/app/apis/entities/generation_result_list/sql/001_list.sql |
