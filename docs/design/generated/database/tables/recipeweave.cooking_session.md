# テーブル仕様: recipeweave.cooking_session

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

調理計画実行

定義元: `database/migrations/002_relational_schema.sql:statement-507`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| menu_id | uuid | 不可 | なし | なし | 対象献立 |
| menu_revision | integer | 不可 | なし | menu_revision &gt; 0 | 献立版 |
| status | text | 不可 | なし | LENGTH(BTRIM(status)) BETWEEN 1 AND 20000; status IN ('planned', 'cooking', 'completed', 'cancelled');  status IN ('planned', 'cooking', 'paused', 'completed', 'cancelled')  | 実行状態 |
| target_at | timestamptz | 可 | なし | なし | 完成希望時刻 |
| planner_version | text | 不可 | なし | LENGTH(BTRIM(planner_version)) BETWEEN 1 AND 20000 | 計画器の版 |
| input_snapshot | jsonb | 不可 | なし | input_snapshot IS NULL OR PG_COLUMN_SIZE(input_snapshot) &lt;= 1048576 | 材料・資源・人数の固定入力 |
| input_hash | char(64) | 不可 | なし | input_hash IS NULL OR input_hash ~ '^[0-9a-f]{64}$' | 入力ハッシュ |
| current_task_index | integer | 不可 | 0 |  current_task_index &gt;= 0  | 調理画面の現在の工程位置（0始まり） |

## 表制約

- `CHECK (menu_revision > 0)`
- `CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000)`
- `CHECK (status IN ('planned', 'cooking', 'completed', 'cancelled'))`
- `CHECK (LENGTH(BTRIM(planner_version)) BETWEEN 1 AND 20000)`
- `CHECK (input_snapshot IS NULL OR PG_COLUMN_SIZE(input_snapshot) <= 1048576)`
- `CHECK (input_hash IS NULL OR input_hash ~ '^[0-9a-f]{64}$')`
- `CHECK ( status IN ('planned', 'cooking', 'paused', 'completed', 'cancelled') )`
- `CHECK ( current_task_index >= 0 )`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_cooking_session_menu_id | False | (menu_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_cooking_session_menu_id | menu_id | menu(id) | CASCADE | RESTRICT | True |

保持・所属領域: owned / 献立

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| export_backup | R | backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q010_export_tables.sql |
| preview_backup | D | backend/src/app/apis/backup/preview_backup/sql/q100_delete_cooking_session.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q100_delete_ingredient_total.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q100_delete_resource_reservation.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q100_delete_session_task.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q100_delete_shopping_item.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q100_delete_task_dependency.sql |
| preview_backup | C | backend/src/app/apis/backup/preview_backup/sql/q200_insert_cooking_session.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q010_export_tables.sql |
| restore_backup | D | backend/src/app/apis/backup/restore_backup/sql/q100_delete_cooking_session.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q100_delete_ingredient_total.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q100_delete_resource_reservation.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q100_delete_session_task.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q100_delete_shopping_item.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q100_delete_task_dependency.sql |
| restore_backup | C | backend/src/app/apis/backup/restore_backup/sql/q200_insert_cooking_session.sql |
| entity_cooking_session_create | C | backend/src/app/apis/entities/cooking_session_create/sql/001_create.sql |
| entity_cooking_session_delete | D | backend/src/app/apis/entities/cooking_session_delete/sql/001_delete.sql |
| entity_cooking_session_get | R | backend/src/app/apis/entities/cooking_session_get/sql/001_get.sql |
| entity_cooking_session_list | R | backend/src/app/apis/entities/cooking_session_list/sql/001_list.sql |
| entity_cooking_session_update | U | backend/src/app/apis/entities/cooking_session_update/sql/001_update.sql |
| entity_ingredient_total_get | R | backend/src/app/apis/entities/ingredient_total_get/sql/001_get.sql |
| entity_ingredient_total_list | R | backend/src/app/apis/entities/ingredient_total_list/sql/001_list.sql |
| entity_resource_reservation_create | R | backend/src/app/apis/entities/resource_reservation_create/sql/002_reference_task_id.sql |
| entity_resource_reservation_delete | R | backend/src/app/apis/entities/resource_reservation_delete/sql/001_delete.sql |
| entity_resource_reservation_get | R | backend/src/app/apis/entities/resource_reservation_get/sql/001_get.sql |
| entity_resource_reservation_list | R | backend/src/app/apis/entities/resource_reservation_list/sql/001_list.sql |
| entity_resource_reservation_update | R | backend/src/app/apis/entities/resource_reservation_update/sql/001_update.sql |
| entity_resource_reservation_update | R | backend/src/app/apis/entities/resource_reservation_update/sql/002_reference_task_id.sql |
| entity_session_task_create | R | backend/src/app/apis/entities/session_task_create/sql/002_reference_session_id.sql |
| entity_session_task_delete | R | backend/src/app/apis/entities/session_task_delete/sql/001_delete.sql |
| entity_session_task_get | R | backend/src/app/apis/entities/session_task_get/sql/001_get.sql |
| entity_session_task_list | R | backend/src/app/apis/entities/session_task_list/sql/001_list.sql |
| entity_session_task_update | R | backend/src/app/apis/entities/session_task_update/sql/001_update.sql |
| entity_session_task_update | R | backend/src/app/apis/entities/session_task_update/sql/002_reference_session_id.sql |
| entity_shopping_item_create | R | backend/src/app/apis/entities/shopping_item_create/sql/002_reference_session_id.sql |
| entity_shopping_item_create | R | backend/src/app/apis/entities/shopping_item_create/sql/003_reference_total_id.sql |
| entity_shopping_item_delete | R | backend/src/app/apis/entities/shopping_item_delete/sql/001_delete.sql |
| entity_shopping_item_get | R | backend/src/app/apis/entities/shopping_item_get/sql/001_get.sql |
| entity_shopping_item_list | R | backend/src/app/apis/entities/shopping_item_list/sql/001_list.sql |
| entity_shopping_item_update | R | backend/src/app/apis/entities/shopping_item_update/sql/001_update.sql |
| entity_shopping_item_update | R | backend/src/app/apis/entities/shopping_item_update/sql/002_reference_session_id.sql |
| entity_shopping_item_update | R | backend/src/app/apis/entities/shopping_item_update/sql/003_reference_total_id.sql |
| entity_task_dependency_create | R | backend/src/app/apis/entities/task_dependency_create/sql/002_reference_before_task_id.sql |
| entity_task_dependency_create | R | backend/src/app/apis/entities/task_dependency_create/sql/003_reference_after_task_id.sql |
| entity_task_dependency_delete | R | backend/src/app/apis/entities/task_dependency_delete/sql/001_delete.sql |
| entity_task_dependency_get | R | backend/src/app/apis/entities/task_dependency_get/sql/001_get.sql |
| entity_task_dependency_list | R | backend/src/app/apis/entities/task_dependency_list/sql/001_list.sql |
| entity_task_dependency_update | R | backend/src/app/apis/entities/task_dependency_update/sql/001_update.sql |
| entity_task_dependency_update | R | backend/src/app/apis/entities/task_dependency_update/sql/002_reference_before_task_id.sql |
| entity_task_dependency_update | R | backend/src/app/apis/entities/task_dependency_update/sql/003_reference_after_task_id.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q001_current.sql |
| create_cooking_session | C | backend/src/app/apis/workspace/create_cooking_session/sql/q025_session.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/update_cooking_session/sql/q001_current.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/update_cooking_session/sql/q002_tasks.sql |
| update_cooking_session | U | backend/src/app/apis/workspace/update_cooking_session/sql/q003_progress.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql |
