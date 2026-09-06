# テーブル仕様: recipeweave.catalog_release

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

カタログ公開版

定義元: `database/migrations/002_relational_schema.sql:statement-13`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| version | text | 不可 | なし | LENGTH(BTRIM(version)) BETWEEN 1 AND 20000 | カタログ版番号 |
| manifest_hash | char(64) | 不可 | なし | manifest_hash IS NULL OR manifest_hash ~ '^[0-9a-f]{64}$' | 採用したID・内容のハッシュ |
| published_at | timestamptz | 可 | なし |  owner_id IS NULL OR published_at IS NULL  | 公開日時 |
| owner_id | uuid | 可 | なし |  owner_id IS NULL OR published_at IS NULL  | 私有カタログの所有者。NULLは共通カタログ |

## 表制約

- `CHECK (LENGTH(BTRIM(version)) BETWEEN 1 AND 20000)`
- `CHECK (manifest_hash IS NULL OR manifest_hash ~ '^[0-9a-f]{64}$')`
- `CHECK ( owner_id IS NULL OR published_at IS NULL )`
- `UNIQUE (version)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_catalog_release_owner_id | False | (owner_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_catalog_release_owner_id | owner_id | app_user(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 共通

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_catalog_release_create | C | backend/src/app/apis/entities/catalog_release_create/sql/001_create.sql |
| entity_catalog_release_get | R | backend/src/app/apis/entities/catalog_release_get/sql/001_get.sql |
| entity_catalog_release_list | R | backend/src/app/apis/entities/catalog_release_list/sql/001_list.sql |
| entity_catalog_release_update | U | backend/src/app/apis/entities/catalog_release_update/sql/001_update.sql |
| commit_receipt | C | backend/src/app/apis/workspace/commit_receipt/sql/q019_private_release.sql |
| create_custom_food | C | backend/src/app/apis/workspace/create_custom_food/sql/q019_private_release.sql |
