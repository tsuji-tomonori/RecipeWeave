# テーブル仕様: recipeweave.food_identity

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

料理同一性上の食品

定義元: `database/migrations/002_relational_schema.sql:statement-611`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変ID |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時 |
| code | text | 不可 | なし | LENGTH(BTRIM(code)) BETWEEN 1 AND 20000 | 形態を横断した食品コード |
| name | text | 不可 | なし | LENGTH(BTRIM(name)) BETWEEN 1 AND 20000 | 食品名 |
| normalizer_version | text | 不可 | なし | LENGTH(BTRIM(normalizer_version)) BETWEEN 1 AND 20000 | 正規化器の版 |

## 表制約

- `CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(normalizer_version)) BETWEEN 1 AND 20000)`
- `UNIQUE (code, normalizer_version)`
- `PRIMARY KEY (id)`

## 索引

独立索引なし。主キー・一意制約の索引は表制約を参照。

## 外部キー

外部キーなし。

保持・所属領域: version / 大規模生成

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_food_identity_create | C | backend/src/app/apis/entities/food_identity_create/sql/001_create.sql |
| entity_food_identity_get | R | backend/src/app/apis/entities/food_identity_get/sql/001_get.sql |
| entity_food_identity_list | R | backend/src/app/apis/entities/food_identity_list/sql/001_list.sql |
