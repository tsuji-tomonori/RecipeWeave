# テーブル仕様: recipeweave.conversion

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

食材形態別換算

定義元: `database/migrations/002_relational_schema.sql:statement-57`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| form_id | uuid | 不可 | なし | なし | 換算対象形態 |
| from_unit_id | uuid | 不可 | なし | from_unit_id &lt;&gt; to_unit_id | 入力単位 |
| to_unit_id | uuid | 不可 | なし | from_unit_id &lt;&gt; to_unit_id | 出力単位 |
| factor | numeric(20,6) | 不可 | なし | factor &gt; 0; factor IS NULL OR factor::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 出力量=入力量×倍率 |
| quality | text | 不可 | なし | LENGTH(BTRIM(quality)) BETWEEN 1 AND 20000; quality IN ('measured', 'manufacturer', 'reference', 'estimated', 'unknown') | 実測・推定区別 |
| source_id | uuid | 可 | なし | なし | 換算根拠 |
| conditions | text | 不可 | なし | LENGTH(BTRIM(conditions)) BETWEEN 1 AND 20000 | サイズ・温度・すり切り等 |
| release_id | uuid | 不可 | なし | なし | 換算版 |

## 表制約

- `CHECK (factor > 0)`
- `CHECK (from_unit_id <> to_unit_id)`
- `CHECK (factor IS NULL OR factor::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (LENGTH(BTRIM(quality)) BETWEEN 1 AND 20000)`
- `CHECK (quality IN ('measured', 'manufacturer', 'reference', 'estimated', 'unknown'))`
- `CHECK (LENGTH(BTRIM(conditions)) BETWEEN 1 AND 20000)`
- `UNIQUE (form_id, from_unit_id, to_unit_id, release_id, conditions)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_conversion_form_id | False | (form_id) |
| ix_conversion_from_unit_id | False | (from_unit_id) |
| ix_conversion_to_unit_id | False | (to_unit_id) |
| ix_conversion_source_id | False | (source_id) |
| ix_conversion_release_id | False | (release_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_conversion_form_id | form_id | food_form(id) | RESTRICT | RESTRICT | True |
| fk_conversion_from_unit_id | from_unit_id | unit(id) | RESTRICT | RESTRICT | True |
| fk_conversion_to_unit_id | to_unit_id | unit(id) | RESTRICT | RESTRICT | True |
| fk_conversion_source_id | source_id | source_record(id) | RESTRICT | RESTRICT | True |
| fk_conversion_release_id | release_id | catalog_release(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 数量

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| export_backup | R | backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q010_export_tables.sql |
| preview_backup | D | backend/src/app/apis/backup/preview_backup/sql/q100_delete_conversion.sql |
| preview_backup | C | backend/src/app/apis/backup/preview_backup/sql/q200_insert_conversion.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q010_export_tables.sql |
| restore_backup | D | backend/src/app/apis/backup/restore_backup/sql/q100_delete_conversion.sql |
| restore_backup | C | backend/src/app/apis/backup/restore_backup/sql/q200_insert_conversion.sql |
| entity_conversion_create | C | backend/src/app/apis/entities/conversion_create/sql/001_create.sql |
| entity_conversion_get | R | backend/src/app/apis/entities/conversion_get/sql/001_get.sql |
| entity_conversion_list | R | backend/src/app/apis/entities/conversion_list/sql/001_list.sql |
| entity_conversion_update | U | backend/src/app/apis/entities/conversion_update/sql/001_update.sql |
