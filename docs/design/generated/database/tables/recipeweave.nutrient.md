# テーブル仕様: recipeweave.nutrient

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

栄養成分種別

定義元: `database/migrations/002_relational_schema.sql:statement-134`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| code | text | 不可 | なし | LENGTH(BTRIM(code)) BETWEEN 1 AND 20000 | energy_kcal等 |
| name | text | 不可 | なし | LENGTH(BTRIM(name)) BETWEEN 1 AND 20000 | エネルギー等 |
| unit_label | text | 不可 | なし | LENGTH(BTRIM(unit_label)) BETWEEN 1 AND 20000 | kcal/g/mg/μg |

## 表制約

- `CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(unit_label)) BETWEEN 1 AND 20000)`
- `UNIQUE (code)`
- `PRIMARY KEY (id)`

## 索引

独立索引なし。主キー・一意制約の索引は表制約を参照。

## 外部キー

外部キーなし。

保持・所属領域: catalog / 食材

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q300_reference_nutrient.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q300_reference_nutrient.sql |
| entity_nutrient_create | C | backend/src/app/apis/entities/nutrient_create/sql/001_create.sql |
| entity_nutrient_get | R | backend/src/app/apis/entities/nutrient_get/sql/001_get.sql |
| entity_nutrient_list | R | backend/src/app/apis/entities/nutrient_list/sql/001_list.sql |
| entity_nutrient_update | U | backend/src/app/apis/entities/nutrient_update/sql/001_update.sql |
