# テーブル仕様: recipeweave.product_preparation_rule

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

商品固有の調理条件

定義元: `database/migrations/002_relational_schema.sql:statement-601`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| product_version_id | uuid | 不可 | なし | なし | 対象商品仕様 |
| operation_id | uuid | 不可 | なし | なし | 対象標準動作 |
| allowed | boolean | 不可 | なし | なし | 表示で許可される方法か |
| use_original_container | boolean | 不可 | なし | なし | 付属容器で調理するか |
| parameter_contract | jsonb | 不可 | なし | parameter_contract IS NULL OR PG_COLUMN_SIZE(parameter_contract) &lt;= 1048576 | 電力・注湯量・時間・蓋などの確定条件 |
| source_id | uuid | 不可 | なし | なし | 商品表示根拠 |

## 表制約

- `CHECK (parameter_contract IS NULL OR PG_COLUMN_SIZE(parameter_contract) <= 1048576)`
- `UNIQUE (product_version_id, operation_id, use_original_container)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_product_preparation_rule_product_version_id | False | ( product_version_id ) |
| ix_product_preparation_rule_operation_id | False | ( operation_id ) |
| ix_product_preparation_rule_source_id | False | ( source_id ) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_product_preparation_rule_product_version_id | product_version_id | product_version(id) | RESTRICT | RESTRICT | True |
| fk_product_preparation_rule_operation_id | operation_id | operation(id) | RESTRICT | RESTRICT | True |
| fk_product_preparation_rule_source_id | source_id | source_record(id) | RESTRICT | RESTRICT | True |

保持・所属領域: version / 食材

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| export_backup | R | backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q010_export_tables.sql |
| preview_backup | D | backend/src/app/apis/backup/preview_backup/sql/q100_delete_product_preparation_rule.sql |
| preview_backup | C | backend/src/app/apis/backup/preview_backup/sql/q200_insert_product_preparation_rule.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q010_export_tables.sql |
| restore_backup | D | backend/src/app/apis/backup/restore_backup/sql/q100_delete_product_preparation_rule.sql |
| restore_backup | C | backend/src/app/apis/backup/restore_backup/sql/q200_insert_product_preparation_rule.sql |
| entity_product_preparation_rule_create | C | backend/src/app/apis/entities/product_preparation_rule_create/sql/001_create.sql |
| entity_product_preparation_rule_get | R | backend/src/app/apis/entities/product_preparation_rule_get/sql/001_get.sql |
| entity_product_preparation_rule_list | R | backend/src/app/apis/entities/product_preparation_rule_list/sql/001_list.sql |
