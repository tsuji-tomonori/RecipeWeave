# テーブル仕様: recipeweave.allergen

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

アレルゲン概念

定義元: `database/migrations/002_relational_schema.sql:statement-111`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| code | text | 不可 | なし | LENGTH(BTRIM(code)) BETWEEN 1 AND 20000 | 固定コード |
| name | text | 不可 | なし | LENGTH(BTRIM(name)) BETWEEN 1 AND 20000 | 名称 |
| source_id | uuid | 可 | なし | なし | 分類出典 |

## 表制約

- `CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000)`
- `UNIQUE (code)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_allergen_source_id | False | (source_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_allergen_source_id | source_id | source_record(id) | RESTRICT | RESTRICT | True |

保持・所属領域: catalog / 食材

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_allergen_create | C | backend/src/app/apis/entities/allergen_create/sql/001_create.sql |
| entity_allergen_get | R | backend/src/app/apis/entities/allergen_get/sql/001_get.sql |
| entity_allergen_list | R | backend/src/app/apis/entities/allergen_list/sql/001_list.sql |
| entity_allergen_update | U | backend/src/app/apis/entities/allergen_update/sql/001_update.sql |
