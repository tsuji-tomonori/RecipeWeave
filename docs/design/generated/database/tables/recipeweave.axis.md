# テーブル仕様: recipeweave.axis

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

組み合わせ軸

定義元: `database/migrations/002_relational_schema.sql:statement-152`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| code | text | 不可 | なし | LENGTH(BTRIM(code)) BETWEEN 1 AND 20000 | 軸コード |
| name | text | 不可 | なし | LENGTH(BTRIM(name)) BETWEEN 1 AND 20000 | 軸名 |
| purpose | text | 不可 | なし | LENGTH(BTRIM(purpose)) BETWEEN 1 AND 20000; purpose IN ('generation', 'search', 'constraint', 'derived', 'presentation') | 生成/検索/制約等 |
| selection | text | 不可 | なし | LENGTH(BTRIM(selection)) BETWEEN 1 AND 20000; selection IN ('single', 'multiple') | 単複 |
| release_id | uuid | 不可 | なし | なし | 定義版 |
| status | text | 不可 | なし | LENGTH(BTRIM(status)) BETWEEN 1 AND 20000; status IN ('active', 'retired') | 採用状態 |

## 表制約

- `CHECK (LENGTH(BTRIM(code)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(purpose)) BETWEEN 1 AND 20000)`
- `CHECK (purpose IN ('generation', 'search', 'constraint', 'derived', 'presentation'))`
- `CHECK (LENGTH(BTRIM(selection)) BETWEEN 1 AND 20000)`
- `CHECK (selection IN ('single', 'multiple'))`
- `CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000)`
- `CHECK (status IN ('active', 'retired'))`
- `UNIQUE (code, release_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_axis_release_id | False | (release_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_axis_release_id | release_id | catalog_release(id) | RESTRICT | RESTRICT | True |

保持・所属領域: catalog / 発想

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_axis_create | C | backend/src/app/apis/entities/axis_create/sql/001_create.sql |
| entity_axis_get | R | backend/src/app/apis/entities/axis_get/sql/001_get.sql |
| entity_axis_list | R | backend/src/app/apis/entities/axis_list/sql/001_list.sql |
| entity_axis_update | U | backend/src/app/apis/entities/axis_update/sql/001_update.sql |
| list_foods | R | backend/src/app/apis/foods/list_foods/sql/001_select_foods.sql |
