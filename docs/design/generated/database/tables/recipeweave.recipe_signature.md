# テーブル仕様: recipeweave.recipe_signature

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

内容重複判定署名

定義元: `database/migrations/002_relational_schema.sql:statement-421`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| recipe_version_id | uuid | 不可 | なし | なし | 対象版 |
| algorithm_version | text | 不可 | なし | LENGTH(BTRIM(algorithm_version)) BETWEEN 1 AND 20000 | 正規化アルゴリズム版 |
| exact_hash | char(64) | 不可 | なし | exact_hash IS NULL OR exact_hash ~ '^[0-9a-f]{64}$' | 材料比率・工程・主要条件のハッシュ |
| canonical_payload | jsonb | 不可 | なし | canonical_payload IS NULL OR PG_COLUMN_SIZE(canonical_payload) &lt;= 1048576 | 正規化対象の監査用内容 |
| cluster_key | text | 不可 | なし | LENGTH(BTRIM(cluster_key)) BETWEEN 1 AND 20000 | 料理近似群キー |

## 表制約

- `CHECK (LENGTH(BTRIM(algorithm_version)) BETWEEN 1 AND 20000)`
- `CHECK (exact_hash IS NULL OR exact_hash ~ '^[0-9a-f]{64}$')`
- `CHECK (canonical_payload IS NULL OR PG_COLUMN_SIZE(canonical_payload) <= 1048576)`
- `CHECK (LENGTH(BTRIM(cluster_key)) BETWEEN 1 AND 20000)`
- `UNIQUE (recipe_version_id, algorithm_version)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_recipe_signature_recipe_version_id | False | ( recipe_version_id ) |
| ix_recipe_signature_search_0 | False | ( algorithm_version, exact_hash ) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_recipe_signature_recipe_version_id | recipe_version_id | recipe_version(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 検索

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_recipe_signature_create | C | backend/src/app/apis/entities/recipe_signature_create/sql/001_create.sql |
| entity_recipe_signature_get | R | backend/src/app/apis/entities/recipe_signature_get/sql/001_get.sql |
| entity_recipe_signature_list | R | backend/src/app/apis/entities/recipe_signature_list/sql/001_list.sql |
