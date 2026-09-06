# テーブル仕様: recipeweave.generation_choice

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

生成軸の選択値

定義元: `database/migrations/002_relational_schema.sql:statement-377`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| job_id | uuid | 不可 | なし | なし | 実行 |
| option_id | uuid | 不可 | なし | なし | 選択した軸候補 |

## 表制約

- `UNIQUE (job_id, option_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_generation_choice_job_id | False | (job_id) |
| ix_generation_choice_option_id | False | (option_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_generation_choice_job_id | job_id | generation_job(id) | RESTRICT | RESTRICT | True |
| fk_generation_choice_option_id | option_id | axis_option(id) | RESTRICT | RESTRICT | True |

保持・所属領域: transient / 生成

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_generation_choice_create | C | backend/src/app/apis/entities/generation_choice_create/sql/001_create.sql |
| entity_generation_choice_get | R | backend/src/app/apis/entities/generation_choice_get/sql/001_get.sql |
| entity_generation_choice_list | R | backend/src/app/apis/entities/generation_choice_list/sql/001_list.sql |
| entity_generation_choice_update | U | backend/src/app/apis/entities/generation_choice_update/sql/001_update.sql |
