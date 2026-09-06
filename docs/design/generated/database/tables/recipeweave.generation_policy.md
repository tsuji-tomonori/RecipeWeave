# テーブル仕様: recipeweave.generation_policy

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

AI生成方針版

定義元: `database/migrations/002_relational_schema.sql:statement-355`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| version | text | 不可 | なし | LENGTH(BTRIM(version)) BETWEEN 1 AND 20000 | 方針識別子 |
| prompt_template | text | 不可 | なし | LENGTH(BTRIM(prompt_template)) BETWEEN 1 AND 20000 | 入力テンプレ |
| model_identifier | text | 不可 | なし | LENGTH(BTRIM(model_identifier)) BETWEEN 1 AND 20000 | 利用モデル名・版 |
| parameter_json | jsonb | 不可 | なし | parameter_json IS NULL OR PG_COLUMN_SIZE(parameter_json) &lt;= 1048576 | temperature/seed等の記録 |
| schema_version | text | 不可 | なし | LENGTH(BTRIM(schema_version)) BETWEEN 1 AND 20000 | 出力JSON契約 |
| release_id | uuid | 不可 | なし | なし | 候補カタログ版 |

## 表制約

- `CHECK (LENGTH(BTRIM(version)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(prompt_template)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(model_identifier)) BETWEEN 1 AND 20000)`
- `CHECK (parameter_json IS NULL OR PG_COLUMN_SIZE(parameter_json) <= 1048576)`
- `CHECK (LENGTH(BTRIM(schema_version)) BETWEEN 1 AND 20000)`
- `UNIQUE (version)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_generation_policy_release_id | False | (release_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_generation_policy_release_id | release_id | catalog_release(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 生成

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_generation_policy_create | C | backend/src/app/apis/entities/generation_policy_create/sql/001_create.sql |
| entity_generation_policy_get | R | backend/src/app/apis/entities/generation_policy_get/sql/001_get.sql |
| entity_generation_policy_list | R | backend/src/app/apis/entities/generation_policy_list/sql/001_list.sql |
