# テーブル仕様: recipeweave.product_component

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

セット内構成品

定義元: `database/migrations/002_relational_schema.sql:statement-101`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| product_version_id | uuid | 不可 | なし | なし | 親商品版 |
| form_id | uuid | 不可 | なし | なし | 麺・ソース・かやく等 |
| name | text | 不可 | なし | LENGTH(BTRIM(name)) BETWEEN 1 AND 20000 | 構成品名 |
| amount | numeric(20,6) | 可 | なし | (amount IS NULL) = (unit_id IS NULL); amount IS NULL OR amount &gt; 0; amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 量（不明はNULL） |
| unit_id | uuid | 可 | なし | (amount IS NULL) = (unit_id IS NULL) | 構成品量単位 |
| quality | text | 不可 | なし | LENGTH(BTRIM(quality)) BETWEEN 1 AND 20000; quality IN ('measured', 'manufacturer', 'reference', 'estimated', 'unknown') | 数量の根拠 |

## 表制約

- `CHECK ((amount IS NULL) = (unit_id IS NULL))`
- `CHECK (amount IS NULL OR amount > 0)`
- `CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000)`
- `CHECK (amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (LENGTH(BTRIM(quality)) BETWEEN 1 AND 20000)`
- `CHECK (quality IN ('measured', 'manufacturer', 'reference', 'estimated', 'unknown'))`
- `UNIQUE (product_version_id, name)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_product_component_product_version_id | False | ( product_version_id ) |
| ix_product_component_form_id | False | (form_id) |
| ix_product_component_unit_id | False | (unit_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_product_component_product_version_id | product_version_id | product_version(id) | RESTRICT | RESTRICT | True |
| fk_product_component_form_id | form_id | food_form(id) | RESTRICT | RESTRICT | True |
| fk_product_component_unit_id | unit_id | unit(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 食材

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_product_component_create | C | backend/src/app/apis/entities/product_component_create/sql/001_create.sql |
| entity_product_component_get | R | backend/src/app/apis/entities/product_component_get/sql/001_get.sql |
| entity_product_component_list | R | backend/src/app/apis/entities/product_component_list/sql/001_list.sql |
