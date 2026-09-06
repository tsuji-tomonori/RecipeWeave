# テーブル仕様: recipeweave.source_record

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

根拠資料

定義元: `database/migrations/002_relational_schema.sql:statement-3`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| title | text | 不可 | なし | LENGTH(BTRIM(title)) BETWEEN 1 AND 20000 | 根拠名 |
| url | text | 可 | なし | なし | 公式資料URL |
| locator | text | 可 | なし | なし | 資料内位置 |
| retrieved_at | timestamptz | 可 | なし | なし | 取得時点 |
| content_hash | char(64) | 可 | なし | content_hash IS NULL OR content_hash ~ '^[0-9a-f]{64}$' | 参照内容のハッシュ |
| license_note | text | 可 | なし | なし | 利用条件・権利確認 |

## 表制約

- `CHECK (LENGTH(BTRIM(title)) BETWEEN 1 AND 20000)`
- `CHECK (content_hash IS NULL OR content_hash ~ '^[0-9a-f]{64}$')`
- `PRIMARY KEY (id)`

## 索引

独立索引なし。主キー・一意制約の索引は表制約を参照。

## 外部キー

外部キーなし。

保持・所属領域: catalog / 共通

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_source_record_create | C | backend/src/app/apis/entities/source_record_create/sql/001_create.sql |
| entity_source_record_get | R | backend/src/app/apis/entities/source_record_get/sql/001_get.sql |
| entity_source_record_list | R | backend/src/app/apis/entities/source_record_list/sql/001_list.sql |
| entity_source_record_update | U | backend/src/app/apis/entities/source_record_update/sql/001_update.sql |
