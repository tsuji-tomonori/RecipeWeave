# テーブル仕様: recipeweave.user_preference

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

ユーザーの嗜好

定義元: `database/migrations/002_relational_schema.sql:statement-447`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| user_id | uuid | 不可 | なし | なし | 利用者 |
| option_id | uuid | 不可 | なし | なし | 味・料理等 |
| weight | numeric(20,6) | 不可 | なし | weight IS NULL OR weight::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 好みの重み |

## 表制約

- `CHECK (weight IS NULL OR weight::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `UNIQUE (user_id, option_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_user_preference_user_id | False | (user_id) |
| ix_user_preference_option_id | False | (option_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_user_preference_user_id | user_id | app_user(id) | CASCADE | RESTRICT | True |
| fk_user_preference_option_id | option_id | axis_option(id) | RESTRICT | RESTRICT | True |

保持・所属領域: owned / 利用者

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_user_preference_create | C | backend/src/app/apis/entities/user_preference_create/sql/001_create.sql |
| entity_user_preference_delete | D | backend/src/app/apis/entities/user_preference_delete/sql/001_delete.sql |
| entity_user_preference_get | R | backend/src/app/apis/entities/user_preference_get/sql/001_get.sql |
| entity_user_preference_list | R | backend/src/app/apis/entities/user_preference_list/sql/001_list.sql |
| entity_user_preference_update | U | backend/src/app/apis/entities/user_preference_update/sql/001_update.sql |
