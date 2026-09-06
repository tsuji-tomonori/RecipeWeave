# テーブル仕様: recipeweave.user_shopping_check

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

調理前の買い物確認

定義元: `database/migrations/003_service_operations.sql:statement-152`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| user_id | uuid | 不可 | なし | なし | 所有者 |
| key | text | 不可 | なし | なし | 買い物対象の安定キー |
| signature | text | 不可 | なし | なし | 数量・商品条件の一致確認用署名 |
| food_id | uuid | 可 | なし | なし | 対象食材 |
| amount | numeric(20,6) | 可 | なし | amount IS NULL OR (amount &gt;= 0 AND amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')); amount IS NULL OR unit_id IS NOT NULL | 必要数量。不明はNULL |
| unit_id | uuid | 可 | なし | amount IS NULL OR unit_id IS NOT NULL | 数量単位 |
| checked_at | timestamptz | 可 | なし | なし | 購入確認日時 |
| archived | boolean | 不可 | FALSE | なし | 保管済みか |

## 表制約

- `CHECK (amount IS NULL OR (amount >= 0 AND amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity')))`
- `CHECK (amount IS NULL OR unit_id IS NOT NULL)`
- `UNIQUE (user_id, key)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_user_shopping_check_user_id | False | (user_id) |
| ix_user_shopping_check_food_id | False | (food_id) |
| ix_user_shopping_check_unit_id | False | (unit_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_user_shopping_check_user_id | user_id | app_user(id) | CASCADE | RESTRICT | True |
| fk_user_shopping_check_food_id | food_id | food(id) | RESTRICT | RESTRICT | True |
| fk_user_shopping_check_unit_id | unit_id | unit(id) | RESTRICT | RESTRICT | True |

保持・所属領域: owned / 利用者操作

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_user_shopping_check_create | C | backend/src/app/apis/entities/user_shopping_check_create/sql/001_create.sql |
| entity_user_shopping_check_delete | D | backend/src/app/apis/entities/user_shopping_check_delete/sql/001_delete.sql |
| entity_user_shopping_check_get | R | backend/src/app/apis/entities/user_shopping_check_get/sql/001_get.sql |
| entity_user_shopping_check_list | R | backend/src/app/apis/entities/user_shopping_check_list/sql/001_list.sql |
| entity_user_shopping_check_update | U | backend/src/app/apis/entities/user_shopping_check_update/sql/001_update.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| put_shopping_checks | D | backend/src/app/apis/workspace/put_shopping_checks/sql/q001_clear.sql |
| put_shopping_checks | C | backend/src/app/apis/workspace/put_shopping_checks/sql/q002_insert.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql |
