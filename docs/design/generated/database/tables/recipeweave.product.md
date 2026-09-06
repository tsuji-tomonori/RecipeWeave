# テーブル仕様: recipeweave.product

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

市販商品識別

定義元: `database/migrations/002_relational_schema.sql:statement-79`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| food_id | uuid | 不可 | なし | なし | 汎用食材との対応 |
| brand | text | 不可 | なし | LENGTH(BTRIM(brand)) BETWEEN 1 AND 20000 | ブランド |
| name | text | 不可 | なし | LENGTH(BTRIM(name)) BETWEEN 1 AND 20000 | 商品名 |
| gtin | text | 可 | なし | なし | JAN等（先頭0保持） |
| status | text | 不可 | なし | LENGTH(BTRIM(status)) BETWEEN 1 AND 20000; status IN ('active', 'retired') | 終売はretired |

## 表制約

- `CHECK (LENGTH(BTRIM(brand)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000)`
- `CHECK (status IN ('active', 'retired'))`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_product_food_id | False | (food_id) |
| uq_product_0 | True | (gtin) WHERE gtin IS NOT NULL |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_product_food_id | food_id | food(id) | RESTRICT | RESTRICT | True |

保持・所属領域: catalog / 食材

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_product_create | C | backend/src/app/apis/entities/product_create/sql/001_create.sql |
| entity_product_get | R | backend/src/app/apis/entities/product_get/sql/001_get.sql |
| entity_product_list | R | backend/src/app/apis/entities/product_list/sql/001_list.sql |
| entity_product_update | U | backend/src/app/apis/entities/product_update/sql/001_update.sql |
