# テーブル仕様: recipeweave.form_yield

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

処理歩留まり

定義元: `database/migrations/002_relational_schema.sql:statement-69`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| input_form_id | uuid | 不可 | なし | input_form_id &lt;&gt; output_form_id | 処理前形態 |
| output_form_id | uuid | 不可 | なし | input_form_id &lt;&gt; output_form_id | 処理後形態 |
| yield_ratio | numeric(20,6) | 不可 | なし | yield_ratio &gt; 0; yield_ratio IS NULL OR yield_ratio::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 出力量/入力量 |
| source_id | uuid | 可 | なし | なし | 根拠 |
| quality | text | 不可 | なし | LENGTH(BTRIM(quality)) BETWEEN 1 AND 20000; quality IN ('measured', 'manufacturer', 'reference', 'estimated', 'unknown') | 精度区分 |
| conditions | text | 不可 | なし | LENGTH(BTRIM(conditions)) BETWEEN 1 AND 20000 | 皮むき・水戻し等の条件 |

## 表制約

- `CHECK (yield_ratio > 0)`
- `CHECK (input_form_id <> output_form_id)`
- `CHECK (yield_ratio IS NULL OR yield_ratio::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `CHECK (LENGTH(BTRIM(quality)) BETWEEN 1 AND 20000)`
- `CHECK (quality IN ('measured', 'manufacturer', 'reference', 'estimated', 'unknown'))`
- `CHECK (LENGTH(BTRIM(conditions)) BETWEEN 1 AND 20000)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_form_yield_input_form_id | False | (input_form_id) |
| ix_form_yield_output_form_id | False | (output_form_id) |
| ix_form_yield_source_id | False | (source_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_form_yield_input_form_id | input_form_id | food_form(id) | RESTRICT | RESTRICT | True |
| fk_form_yield_output_form_id | output_form_id | food_form(id) | RESTRICT | RESTRICT | True |
| fk_form_yield_source_id | source_id | source_record(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 数量

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| export_backup | R | backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q010_export_tables.sql |
| preview_backup | D | backend/src/app/apis/backup/preview_backup/sql/q100_delete_form_yield.sql |
| preview_backup | C | backend/src/app/apis/backup/preview_backup/sql/q200_insert_form_yield.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q010_export_tables.sql |
| restore_backup | D | backend/src/app/apis/backup/restore_backup/sql/q100_delete_form_yield.sql |
| restore_backup | C | backend/src/app/apis/backup/restore_backup/sql/q200_insert_form_yield.sql |
| entity_form_yield_create | C | backend/src/app/apis/entities/form_yield_create/sql/001_create.sql |
| entity_form_yield_get | R | backend/src/app/apis/entities/form_yield_get/sql/001_get.sql |
| entity_form_yield_list | R | backend/src/app/apis/entities/form_yield_list/sql/001_list.sql |
