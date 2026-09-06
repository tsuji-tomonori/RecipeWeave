# テーブル仕様: recipeweave.candidate_attempt

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

試行済み設計点の台帳

定義元: `database/migrations/002_relational_schema.sql:statement-648`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変ID |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時 |
| template_id | uuid | 不可 | なし | なし | 定義版 |
| ordinal | bigint | 不可 | なし | ordinal &gt;= 0 | 設計点の序数 |
| design_key | char(64) | 不可 | なし | design_key IS NULL OR design_key ~ '^[0-9a-f]{64}$' | 正規化した設計キー |
| job_id | uuid | 可 | なし | なし | 生成ジョブ |
| state | text | 不可 | なし | state &lt;&gt; 'accepted' OR recipe_version_id IS NOT NULL; LENGTH(BTRIM(state)) BETWEEN 1 AND 20000; state IN ('pending', 'invalid', 'generated', 'duplicate', 'accepted', 'failed') | 候補の段階 |
| reason_code | text | 可 | なし | なし | 棄却理由 |
| recipe_version_id | uuid | 可 | なし | state &lt;&gt; 'accepted' OR recipe_version_id IS NOT NULL | 採用した版 |
| attempts | integer | 不可 | なし | attempts BETWEEN 0 AND 5 | 試行上限（暫定） |

## 表制約

- `CHECK (ordinal >= 0)`
- `CHECK (attempts BETWEEN 0 AND 5)`
- `CHECK (state <> 'accepted' OR recipe_version_id IS NOT NULL)`
- `CHECK (design_key IS NULL OR design_key ~ '^[0-9a-f]{64}$')`
- `CHECK (LENGTH(BTRIM(state)) BETWEEN 1 AND 20000)`
- `CHECK (state IN ('pending', 'invalid', 'generated', 'duplicate', 'accepted', 'failed'))`
- `UNIQUE (template_id, ordinal)`
- `UNIQUE (template_id, design_key)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_candidate_attempt_template_id | False | (template_id) |
| ix_candidate_attempt_job_id | False | (job_id) |
| ix_candidate_attempt_recipe_version_id | False | ( recipe_version_id ) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_candidate_attempt_template_id | template_id | generation_template(id) | RESTRICT | RESTRICT | True |
| fk_candidate_attempt_job_id | job_id | generation_job(id) | SET NULL | RESTRICT | True |
| fk_candidate_attempt_recipe_version_id | recipe_version_id | recipe_version(id) | RESTRICT | RESTRICT | True |

保持・所属領域: transient / 大規模生成

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_candidate_attempt_create | C | backend/src/app/apis/entities/candidate_attempt_create/sql/001_create.sql |
| entity_candidate_attempt_get | R | backend/src/app/apis/entities/candidate_attempt_get/sql/001_get.sql |
| entity_candidate_attempt_list | R | backend/src/app/apis/entities/candidate_attempt_list/sql/001_list.sql |
| entity_candidate_attempt_update | U | backend/src/app/apis/entities/candidate_attempt_update/sql/001_update.sql |
