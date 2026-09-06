# テーブル仕様: recipeweave.food_allergen

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

食材アレルゲン知識

定義元: `database/migrations/002_relational_schema.sql:statement-118`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| form_id | uuid | 不可 | なし | なし | 食材形態 |
| allergen_id | uuid | 不可 | なし | なし | 対象物質 |
| presence | text | 不可 | なし | LENGTH(BTRIM(presence)) BETWEEN 1 AND 20000; presence IN ('contains', 'may_contain', 'absent_verified', 'unknown') | 含有・不明 |
| source_id | uuid | 不可 | なし | なし | 判断根拠 |

## 表制約

- `CHECK (LENGTH(BTRIM(presence)) BETWEEN 1 AND 20000)`
- `CHECK (presence IN ('contains', 'may_contain', 'absent_verified', 'unknown'))`
- `UNIQUE (form_id, allergen_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_food_allergen_form_id | False | (form_id) |
| ix_food_allergen_allergen_id | False | (allergen_id) |
| ix_food_allergen_source_id | False | (source_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_food_allergen_form_id | form_id | food_form(id) | RESTRICT | RESTRICT | True |
| fk_food_allergen_allergen_id | allergen_id | allergen(id) | RESTRICT | RESTRICT | True |
| fk_food_allergen_source_id | source_id | source_record(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 食材

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| export_backup | R | backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q010_export_tables.sql |
| preview_backup | D | backend/src/app/apis/backup/preview_backup/sql/q100_delete_food_allergen.sql |
| preview_backup | C | backend/src/app/apis/backup/preview_backup/sql/q200_insert_food_allergen.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q010_export_tables.sql |
| restore_backup | D | backend/src/app/apis/backup/restore_backup/sql/q100_delete_food_allergen.sql |
| restore_backup | C | backend/src/app/apis/backup/restore_backup/sql/q200_insert_food_allergen.sql |
| entity_food_allergen_create | C | backend/src/app/apis/entities/food_allergen_create/sql/001_create.sql |
| entity_food_allergen_get | R | backend/src/app/apis/entities/food_allergen_get/sql/001_get.sql |
| entity_food_allergen_list | R | backend/src/app/apis/entities/food_allergen_list/sql/001_list.sql |
