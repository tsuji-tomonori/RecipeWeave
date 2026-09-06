# テーブル仕様: recipeweave.nutrition_fact

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

形態・商品別栄養値

定義元: `database/migrations/002_relational_schema.sql:statement-141`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| form_id | uuid | 可 | なし | NUM_NONNULLS(form_id, product_version_id) = 1 | 汎用形態 |
| product_version_id | uuid | 可 | なし | NUM_NONNULLS(form_id, product_version_id) = 1 | 商品仕様 |
| nutrient_id | uuid | 不可 | なし | なし | 栄養成分 |
| amount | numeric(20,6) | 不可 | なし | amount &gt;= 0; amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 基準量あたり成分量 |
| basis_amount | numeric(20,6) | 不可 | なし | basis_amount &gt; 0; basis_amount IS NULL OR basis_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 基準量 |
| basis_unit_id | uuid | 不可 | なし | なし | 基準単位 |
| source_id | uuid | 不可 | なし | なし | 出典 |

## 表制約

- `CHECK (NUM_NONNULLS(form_id, product_version_id) = 1)`
- `CHECK (amount >= 0)`
- `CHECK (basis_amount > 0)`
- `CHECK (amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (basis_amount IS NULL OR basis_amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_nutrition_fact_form_id | False | (form_id) |
| ix_nutrition_fact_product_version_id | False | ( product_version_id ) |
| ix_nutrition_fact_nutrient_id | False | (nutrient_id) |
| ix_nutrition_fact_basis_unit_id | False | (basis_unit_id) |
| ix_nutrition_fact_source_id | False | (source_id) |
| uq_nutrition_fact_0 | True | ( form_id, nutrient_id, source_id ) WHERE form_id IS NOT NULL |
| uq_nutrition_fact_1 | True | ( product_version_id, nutrient_id, source_id ) WHERE product_version_id IS NOT NULL |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_nutrition_fact_form_id | form_id | food_form(id) | RESTRICT | RESTRICT | True |
| fk_nutrition_fact_product_version_id | product_version_id | product_version(id) | RESTRICT | RESTRICT | True |
| fk_nutrition_fact_nutrient_id | nutrient_id | nutrient(id) | RESTRICT | RESTRICT | True |
| fk_nutrition_fact_basis_unit_id | basis_unit_id | unit(id) | RESTRICT | RESTRICT | True |
| fk_nutrition_fact_source_id | source_id | source_record(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 食材

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_nutrition_fact_create | C | backend/src/app/apis/entities/nutrition_fact_create/sql/001_create.sql |
| entity_nutrition_fact_get | R | backend/src/app/apis/entities/nutrition_fact_get/sql/001_get.sql |
| entity_nutrition_fact_list | R | backend/src/app/apis/entities/nutrition_fact_list/sql/001_list.sql |
