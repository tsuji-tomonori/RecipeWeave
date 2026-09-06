# テーブル仕様: recipeweave.generation_template

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

列挙テンプレート版

定義元: `database/migrations/002_relational_schema.sql:statement-626`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変ID |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時 |
| code | text | 不可 | なし | LENGTH(BTRIM(code)) BETWEEN 1 AND 20000 | テンプレートコード |
| version | integer | 不可 | なし | version &gt; 0 | 定義版 |
| release_id | uuid | 不可 | なし | なし | カタログ版 |
| contract | jsonb | 不可 | なし | contract IS NULL OR PG_COLUMN_SIZE(contract) &lt;= 1048576 | 主副材の許可集合・k・味付・経路 |
| candidate_count | bigint | 不可 | なし | candidate_count &gt;= 0 | この定義の正確な設計点数 |
| contract_hash | char(64) | 不可 | なし | contract_hash IS NULL OR contract_hash ~ '^[0-9a-f]{64}$' | 定義ハッシュ |

## 表制約

- `CHECK (version > 0)`
- `CHECK (candidate_count >= 0)`
- `CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000)`
- `CHECK (contract IS NULL OR PG_COLUMN_SIZE(contract) <= 1048576)`
- `CHECK (contract_hash IS NULL OR contract_hash ~ '^[0-9a-f]{64}$')`
- `UNIQUE (code, version)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_generation_template_release_id | False | (release_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_generation_template_release_id | release_id | catalog_release(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 大規模生成

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_generation_template_create | C | backend/src/app/apis/entities/generation_template_create/sql/001_create.sql |
| entity_generation_template_get | R | backend/src/app/apis/entities/generation_template_get/sql/001_get.sql |
| entity_generation_template_list | R | backend/src/app/apis/entities/generation_template_list/sql/001_list.sql |
