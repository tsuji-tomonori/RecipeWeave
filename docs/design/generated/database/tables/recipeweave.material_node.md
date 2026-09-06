# テーブル仕様: recipeweave.material_node

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

材料・中間物ノード

定義元: `database/migrations/002_relational_schema.sql:statement-290`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| recipe_version_id | uuid | 不可 | なし | なし | 親版 |
| name | text | 不可 | なし | LENGTH(BTRIM(name)) BETWEEN 1 AND 20000 | 切ったにんじん・合わせ調味料等 |
| kind | text | 不可 | なし | (kind = 'ingredient' AND ingredient_line_id IS NOT NULL AND producer_step_id IS NULL) OR (kind &lt;&gt; 'ingredient' AND ingredient_line_id IS NULL AND producer_step_id IS NOT NULL); LENGTH(BTRIM(kind)) BETWEEN 1 AND 20000; kind IN ('ingredient', 'intermediate', 'dish', 'waste') | 入力/中間/完成/廃棄 |
| ingredient_line_id | uuid | 可 | なし | (kind = 'ingredient' AND ingredient_line_id IS NOT NULL AND producer_step_id IS NULL) OR (kind &lt;&gt; 'ingredient' AND ingredient_line_id IS NULL AND producer_step_id IS NOT NULL) | 原材料明細 |
| producer_step_id | uuid | 可 | なし | (kind = 'ingredient' AND ingredient_line_id IS NOT NULL AND producer_step_id IS NULL) OR (kind &lt;&gt; 'ingredient' AND ingredient_line_id IS NULL AND producer_step_id IS NOT NULL) | 生成工程 |
| amount | numeric(20,6) | 可 | なし | amount IS NULL OR amount &gt; 0; (amount IS NULL) = (unit_id IS NULL); amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 予定生成量 |
| unit_id | uuid | 可 | なし | (amount IS NULL) = (unit_id IS NULL) | 生成量単位 |

## 表制約

- `CHECK ((kind = 'ingredient' AND ingredient_line_id IS NOT NULL AND producer_step_id IS NULL) OR (kind <> 'ingredient' AND ingredient_line_id IS NULL AND producer_step_id IS NOT NULL))`
- `CHECK (amount IS NULL OR amount > 0)`
- `CHECK ((amount IS NULL) = (unit_id IS NULL))`
- `CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(kind)) BETWEEN 1 AND 20000)`
- `CHECK (kind IN ('ingredient', 'intermediate', 'dish', 'waste'))`
- `CHECK (amount IS NULL OR amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_material_node_recipe_version_id | False | (recipe_version_id) |
| ix_material_node_ingredient_line_id | False | (ingredient_line_id) |
| ix_material_node_producer_step_id | False | (producer_step_id) |
| ix_material_node_unit_id | False | (unit_id) |
| uq_material_node_0 | True | ( ingredient_line_id ) WHERE ingredient_line_id IS NOT NULL |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_material_node_recipe_version_id | recipe_version_id | recipe_version(id) | RESTRICT | RESTRICT | True |
| fk_material_node_ingredient_line_id | ingredient_line_id | recipe_ingredient(id) | RESTRICT | RESTRICT | True |
| fk_material_node_producer_step_id | producer_step_id | recipe_step(id) | RESTRICT | RESTRICT | True |
| fk_material_node_unit_id | unit_id | unit(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 工程

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_material_node_create | C | backend/src/app/apis/entities/material_node_create/sql/001_create.sql |
| entity_material_node_get | R | backend/src/app/apis/entities/material_node_get/sql/001_get.sql |
| entity_material_node_list | R | backend/src/app/apis/entities/material_node_list/sql/001_list.sql |
| entity_material_node_update | U | backend/src/app/apis/entities/material_node_update/sql/001_update.sql |
