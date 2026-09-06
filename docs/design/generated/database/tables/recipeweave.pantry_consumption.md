# テーブル仕様: recipeweave.pantry_consumption

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

調理による在庫消費の冪等台帳

定義元: `database/migrations/003_service_operations.sql:statement-43`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| user_id | uuid | 不可 | なし | なし | 所有者 |
| session_id | uuid | 不可 | なし | なし | 消費した調理セッション |
| lot_id | uuid | 不可 | なし | なし | 消費元ロット |
| amount | numeric(20,6) | 不可 | なし | amount &gt; 0; amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 消費数量 |
| unit_id | uuid | 不可 | なし | なし | 消費数量の単位 |

## 表制約

- `CHECK (amount > 0)`
- `CHECK (amount::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `UNIQUE (session_id, lot_id)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_pantry_consumption_user_id | False | (user_id) |
| ix_pantry_consumption_session_id | False | (session_id) |
| ix_pantry_consumption_lot_id | False | (lot_id) |
| ix_pantry_consumption_unit_id | False | (unit_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_pantry_consumption_user_id | user_id | app_user(id) | CASCADE | RESTRICT | True |
| fk_pantry_consumption_session_id | session_id | cooking_session(id) | CASCADE | RESTRICT | True |
| fk_pantry_consumption_lot_id | lot_id | pantry_lot(id) | RESTRICT | RESTRICT | True |
| fk_pantry_consumption_unit_id | unit_id | unit(id) | RESTRICT | RESTRICT | True |

保持・所属領域: owned / 利用者操作

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_pantry_consumption_get | R | backend/src/app/apis/entities/pantry_consumption_get/sql/001_get.sql |
| entity_pantry_consumption_list | R | backend/src/app/apis/entities/pantry_consumption_list/sql/001_list.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| undo_receipt | R | backend/src/app/apis/workspace/undo_receipt/sql/q002_eligible_lots.sql |
| update_cooking_session | C | backend/src/app/apis/workspace/update_cooking_session/sql/q009_ledger.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql |
