# テーブル仕様: recipeweave.recipe_search_document

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

公開検索用文書

定義元: `database/migrations/002_relational_schema.sql:statement-660`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変ID |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時 |
| recipe_id | uuid | 不可 | なし | なし | 同一性単位で1件 |
| published_version_id | uuid | 不可 | なし | なし | 検索対象の公開版 |
| projection_version | text | 不可 | なし | LENGTH(BTRIM(projection_version)) BETWEEN 1 AND 20000 | 検索文書の生成器版 |
| display_title | text | 不可 | なし | LENGTH(BTRIM(display_title)) BETWEEN 1 AND 20000 | 表示タイトル |
| food_identity_ids | uuid[] | 不可 | なし | なし | 検索用食品ID集合 |
| facet_option_ids | uuid[] | 不可 | なし | なし | 料理・味等の検索軸 |
| search_text | text | 不可 | なし | LENGTH(BTRIM(search_text)) BETWEEN 1 AND 20000 | 検索用本文 |
| eligible | boolean | 不可 | なし | なし | 公開可能か |
| source_hash | char(64) | 不可 | なし | source_hash IS NULL OR source_hash ~ '^[0-9a-f]{64}$' | 正本一致確認 |
| projected_at | timestamptz | 不可 | なし | なし | 更新時点 |

## 表制約

- `CHECK (LENGTH(BTRIM(projection_version)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(display_title)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(search_text)) BETWEEN 1 AND 20000)`
- `CHECK (source_hash IS NULL OR source_hash ~ '^[0-9a-f]{64}$')`
- `UNIQUE (recipe_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_recipe_search_document_recipe_id | False | (recipe_id) |
| ix_recipe_search_document_published_version_id | False | ( published_version_id ) |
| ix_recipe_search_document_search_0 | False | USING gin ( food_identity_ids ) |
| ix_recipe_search_document_search_1 | False | USING gin ( facet_option_ids ) |
| ix_recipe_search_document_search_2 | False | USING gin ( TO_TSVECTOR('simple', search_text) ) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_recipe_search_document_recipe_id | recipe_id | recipe(id) | RESTRICT | RESTRICT | True |
| fk_recipe_search_document_published_version_id | published_version_id | recipe_version(id) | RESTRICT | RESTRICT | True |

保持・所属領域: transient / 大規模生成

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_recipe_search_document_get | R | backend/src/app/apis/entities/recipe_search_document_get/sql/001_get.sql |
| entity_recipe_search_document_list | R | backend/src/app/apis/entities/recipe_search_document_list/sql/001_list.sql |
