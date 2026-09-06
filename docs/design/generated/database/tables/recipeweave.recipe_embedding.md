# テーブル仕様: recipeweave.recipe_embedding

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

近似検索用特徴量

定義元: `database/migrations/002_relational_schema.sql:statement-674`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変ID |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時 |
| recipe_version_id | uuid | 不可 | なし | なし | 対象版 |
| model_version | text | 不可 | なし | LENGTH(BTRIM(model_version)) BETWEEN 1 AND 20000 | 埋め込みモデル固定版 |
| content_hash | char(64) | 不可 | なし | content_hash IS NULL OR content_hash ~ '^[0-9a-f]{64}$' | 入力内容ハッシュ |
| embedding | vector(768) | 不可 | なし | なし | 仮定768次元float32 |
| created_for_index | text | 不可 | なし | LENGTH(BTRIM(created_for_index)) BETWEEN 1 AND 20000 | 検索索引版 |

## 表制約

- `CHECK (LENGTH(BTRIM(model_version)) BETWEEN 1 AND 20000)`
- `CHECK (content_hash IS NULL OR content_hash ~ '^[0-9a-f]{64}$')`
- `CHECK (LENGTH(BTRIM(created_for_index)) BETWEEN 1 AND 20000)`
- `UNIQUE (recipe_version_id, model_version)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_recipe_embedding_recipe_version_id | False | ( recipe_version_id ) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_recipe_embedding_recipe_version_id | recipe_version_id | recipe_version(id) | RESTRICT | RESTRICT | True |

保持・所属領域: transient / 大規模生成

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_recipe_embedding_create | C | backend/src/app/apis/entities/recipe_embedding_create/sql/001_create.sql |
| entity_recipe_embedding_get | R | backend/src/app/apis/entities/recipe_embedding_get/sql/001_get.sql |
| entity_recipe_embedding_list | R | backend/src/app/apis/entities/recipe_embedding_list/sql/001_list.sql |
| entity_recipe_embedding_update | U | backend/src/app/apis/entities/recipe_embedding_update/sql/001_update.sql |
