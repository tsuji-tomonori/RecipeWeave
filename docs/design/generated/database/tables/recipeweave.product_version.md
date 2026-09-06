# テーブル仕様: recipeweave.product_version

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

商品仕様版

定義元: `database/migrations/002_relational_schema.sql:statement-88`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| product_id | uuid | 不可 | なし | なし | 商品 |
| version | integer | 不可 | なし | version &gt; 0 | 仕様版 |
| form_id | uuid | 不可 | なし | なし | 販売形態 |
| net_amount | numeric(20,6) | 不可 | なし | net_amount &gt; 0; drain_amount IS NULL OR (drain_amount &gt; 0 AND drain_amount &lt;= net_amount); net_amount IS NULL OR net_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 1包装の内容量 |
| unit_id | uuid | 不可 | なし | なし | 内容量単位 |
| drain_amount | numeric(20,6) | 可 | なし | drain_amount IS NULL OR (drain_amount &gt; 0 AND drain_amount &lt;= net_amount); drain_amount IS NULL OR drain_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 固形量 |
| source_id | uuid | 不可 | なし | なし | メーカー表示根拠 |
| preparation_note | text | 不可 | なし | LENGTH(BTRIM(preparation_note)) BETWEEN 1 AND 20000 | 容器・加熱方式・表示手順 |
| valid_from | date | 不可 | なし | なし | 適用開始日 |

## 表制約

- `CHECK (version > 0)`
- `CHECK (net_amount > 0)`
- `CHECK (drain_amount IS NULL OR (drain_amount > 0 AND drain_amount <= net_amount))`
- `CHECK (net_amount IS NULL OR net_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (drain_amount IS NULL OR drain_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (LENGTH(BTRIM(preparation_note)) BETWEEN 1 AND 20000)`
- `UNIQUE (product_id, version)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_product_version_product_id | False | (product_id) |
| ix_product_version_form_id | False | (form_id) |
| ix_product_version_unit_id | False | (unit_id) |
| ix_product_version_source_id | False | (source_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_product_version_product_id | product_id | product(id) | RESTRICT | RESTRICT | True |
| fk_product_version_form_id | form_id | food_form(id) | RESTRICT | RESTRICT | True |
| fk_product_version_unit_id | unit_id | unit(id) | RESTRICT | RESTRICT | True |
| fk_product_version_source_id | source_id | source_record(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 食材

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_product_version_create | C | backend/src/app/apis/entities/product_version_create/sql/001_create.sql |
| entity_product_version_get | R | backend/src/app/apis/entities/product_version_get/sql/001_get.sql |
| entity_product_version_list | R | backend/src/app/apis/entities/product_version_list/sql/001_list.sql |
