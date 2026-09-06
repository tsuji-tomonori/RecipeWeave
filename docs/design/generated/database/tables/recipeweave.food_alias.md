# テーブル仕様: recipeweave.food_alias

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

食材別名

定義元: `database/migrations/002_relational_schema.sql:statement-40`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| food_id | uuid | 不可 | なし | なし | 正規食材 |
| alias | text | 不可 | なし | LENGTH(BTRIM(alias)) BETWEEN 1 AND 20000; CHAR_LENGTH(alias) &lt;= 500 | 別名・かな |
| locale | text | 不可 | なし | LENGTH(BTRIM(locale)) BETWEEN 1 AND 20000 | 言語・地域 |

## 表制約

- `CHECK (LENGTH(BTRIM(alias)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(locale)) BETWEEN 1 AND 20000)`
- `CHECK (CHAR_LENGTH(alias) <= 500)`
- `UNIQUE (food_id, alias, locale)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_food_alias_food_id | False | (food_id) |
| ix_food_alias_search_0 | False | (alias, locale) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_food_alias_food_id | food_id | food(id) | RESTRICT | RESTRICT | True |

保持・所属領域: catalog / 食材

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_food_alias_create | C | backend/src/app/apis/entities/food_alias_create/sql/001_create.sql |
| entity_food_alias_get | R | backend/src/app/apis/entities/food_alias_get/sql/001_get.sql |
| entity_food_alias_list | R | backend/src/app/apis/entities/food_alias_list/sql/001_list.sql |
| entity_food_alias_update | U | backend/src/app/apis/entities/food_alias_update/sql/001_update.sql |
| list_foods | R | backend/src/app/apis/foods/list_foods/sql/001_select_foods.sql |
