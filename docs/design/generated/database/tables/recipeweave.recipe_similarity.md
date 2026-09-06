# テーブル仕様: recipeweave.recipe_similarity

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

近似レシピ関係

定義元: `database/migrations/002_relational_schema.sql:statement-430`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| left_version_id | uuid | 不可 | なし | left_version_id &lt; right_version_id | 左版 |
| right_version_id | uuid | 不可 | なし | left_version_id &lt; right_version_id | 右版 |
| algorithm_version | text | 不可 | なし | LENGTH(BTRIM(algorithm_version)) BETWEEN 1 AND 20000 | 評価器版 |
| score | numeric(20,6) | 不可 | なし | score &gt;= 0 AND score &lt;= 1; score IS NULL OR score::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 類似度0..1 |
| explanation | text | 不可 | なし | LENGTH(BTRIM(explanation)) BETWEEN 1 AND 20000 | 材料/味付/工程の一致差分 |

## 表制約

- `CHECK (left_version_id < right_version_id)`
- `CHECK (score >= 0 AND score <= 1)`
- `CHECK (LENGTH(BTRIM(algorithm_version)) BETWEEN 1 AND 20000)`
- `CHECK (score IS NULL OR score::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (LENGTH(BTRIM(explanation)) BETWEEN 1 AND 20000)`
- `UNIQUE (left_version_id, right_version_id, algorithm_version)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_recipe_similarity_left_version_id | False | ( left_version_id ) |
| ix_recipe_similarity_right_version_id | False | ( right_version_id ) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_recipe_similarity_left_version_id | left_version_id | recipe_version(id) | RESTRICT | RESTRICT | True |
| fk_recipe_similarity_right_version_id | right_version_id | recipe_version(id) | RESTRICT | RESTRICT | True |

保持・所属領域: transient / 検索

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_recipe_similarity_create | C | backend/src/app/apis/entities/recipe_similarity_create/sql/001_create.sql |
| entity_recipe_similarity_get | R | backend/src/app/apis/entities/recipe_similarity_get/sql/001_get.sql |
| entity_recipe_similarity_list | R | backend/src/app/apis/entities/recipe_similarity_list/sql/001_list.sql |
| entity_recipe_similarity_update | U | backend/src/app/apis/entities/recipe_similarity_update/sql/001_update.sql |
