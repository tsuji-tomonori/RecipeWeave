# テーブル仕様: recipeweave.compatibility_rule

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

組み合わせ・公開ルール

定義元: `database/migrations/002_relational_schema.sql:statement-400`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| code | text | 不可 | なし | LENGTH(BTRIM(code)) BETWEEN 1 AND 20000 | 規則コード |
| version | integer | 不可 | なし | version &gt; 0 | 規則版 |
| severity | text | 不可 | なし | LENGTH(BTRIM(severity)) BETWEEN 1 AND 20000; severity IN ('block', 'review', 'score') | 除外/保留/順位 |
| predicate | jsonb | 不可 | なし | predicate IS NULL OR PG_COLUMN_SIZE(predicate) &lt;= 1048576 | 型付き条件式 |
| message | text | 不可 | なし | LENGTH(BTRIM(message)) BETWEEN 1 AND 20000 | 理由 |
| source_id | uuid | 可 | なし | なし | 根拠 |
| status | text | 不可 | なし | LENGTH(BTRIM(status)) BETWEEN 1 AND 20000; status IN ('active', 'retired') | 利用状態 |

## 表制約

- `CHECK (version > 0)`
- `CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(severity)) BETWEEN 1 AND 20000)`
- `CHECK (severity IN ('block', 'review', 'score'))`
- `CHECK (predicate IS NULL OR PG_COLUMN_SIZE(predicate) <= 1048576)`
- `CHECK (LENGTH(BTRIM(message)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000)`
- `CHECK (status IN ('active', 'retired'))`
- `UNIQUE (code, version)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_compatibility_rule_source_id | False | (source_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_compatibility_rule_source_id | source_id | source_record(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 生成

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_compatibility_rule_create | C | backend/src/app/apis/entities/compatibility_rule_create/sql/001_create.sql |
| entity_compatibility_rule_get | R | backend/src/app/apis/entities/compatibility_rule_get/sql/001_get.sql |
| entity_compatibility_rule_list | R | backend/src/app/apis/entities/compatibility_rule_list/sql/001_list.sql |
| get_recipe | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| list_recipes | R | backend/src/app/apis/recipes/list_recipes/sql/001_select_recipes.sql |
| random_recipe | R | backend/src/app/apis/recipes/random_recipe/sql/001_random_recipe.sql |
| preview_cooking_plan | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
