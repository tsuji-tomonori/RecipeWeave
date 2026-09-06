# テーブル仕様: recipeweave.session_task

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

展開済み工程

定義元: `database/migrations/002_relational_schema.sql:statement-518`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| session_id | uuid | 不可 | なし | なし | 実行 |
| menu_item_id | uuid | 不可 | なし | なし | 料理 |
| step_id | uuid | 不可 | なし | なし | 元工程 |
| batch_no | integer | 不可 | なし | batch_no &gt; 0 | 容量分割した回 |
| planned_start_s | integer | 不可 | なし | planned_start_s &gt;= 0; planned_end_s &gt;= planned_start_s;  (duration_source = 'recipe_rule' AND confirmed_duration_s IS NULL) OR ( duration_source = 'user_estimate' AND confirmed_duration_s IS NOT NULL AND planned_end_s - planned_start_s = confirmed_duration_s )  | 開始相対秒 |
| planned_end_s | integer | 不可 | なし | planned_end_s &gt;= planned_start_s;  (duration_source = 'recipe_rule' AND confirmed_duration_s IS NULL) OR ( duration_source = 'user_estimate' AND confirmed_duration_s IS NOT NULL AND planned_end_s - planned_start_s = confirmed_duration_s )  | 終了相対秒 |
| status | text | 不可 | なし | LENGTH(BTRIM(status)) BETWEEN 1 AND 20000; status IN ('pending', 'running', 'completed', 'skipped') | 進捗 |
| actual_start_at | timestamptz | 可 | なし | actual_end_at IS NULL OR (actual_start_at IS NOT NULL AND actual_end_at &gt;= actual_start_at) | 実開始 |
| actual_end_at | timestamptz | 可 | なし | actual_end_at IS NULL OR (actual_start_at IS NOT NULL AND actual_end_at &gt;= actual_start_at) | 実完了 |
| timer_started_at | timestamptz | 可 | なし |  timer_started_at IS NULL OR timer_duration_s IS NOT NULL  | 稼働中タイマーの開始日時 |
| timer_duration_s | integer | 可 | なし |  timer_duration_s IS NULL OR timer_duration_s &gt;= 0 ;  timer_started_at IS NULL OR timer_duration_s IS NOT NULL  | 利用者が設定したタイマー秒数 |
| duration_source | text | 不可 | 'recipe_rule' | duration_source IN ('recipe_rule', 'user_estimate');  (duration_source = 'recipe_rule' AND confirmed_duration_s IS NULL) OR ( duration_source = 'user_estimate' AND confirmed_duration_s IS NOT NULL AND planned_end_s - planned_start_s = confirmed_duration_s )  | 計画時間の根拠。料理の時間規則または利用者が確認した見積り |
| confirmed_duration_s | integer | 可 | なし | confirmed_duration_s IS NULL OR confirmed_duration_s BETWEEN 1 AND 86400;  (duration_source = 'recipe_rule' AND confirmed_duration_s IS NULL) OR ( duration_source = 'user_estimate' AND confirmed_duration_s IS NOT NULL AND planned_end_s - planned_start_s = confirmed_duration_s )  | 利用者が確認した工程の見積り秒数。実測値ではなく、計画後は変更しない |

## 表制約

- `CHECK (batch_no > 0)`
- `CHECK (planned_start_s >= 0)`
- `CHECK (planned_end_s >= planned_start_s)`
- `CHECK (actual_end_at IS NULL OR (actual_start_at IS NOT NULL AND actual_end_at >= actual_start_at))`
- `CHECK (LENGTH(BTRIM(status)) BETWEEN 1 AND 20000)`
- `CHECK (status IN ('pending', 'running', 'completed', 'skipped'))`
- `CHECK ( timer_duration_s IS NULL OR timer_duration_s >= 0 )`
- `CHECK ( timer_started_at IS NULL OR timer_duration_s IS NOT NULL )`
- `CHECK (duration_source IN ('recipe_rule', 'user_estimate'))`
- `CHECK (confirmed_duration_s IS NULL OR confirmed_duration_s BETWEEN 1 AND 86400)`
- `CHECK ( (duration_source = 'recipe_rule' AND confirmed_duration_s IS NULL) OR ( duration_source = 'user_estimate' AND confirmed_duration_s IS NOT NULL AND planned_end_s - planned_start_s = confirmed_duration_s ) )`
- `UNIQUE (session_id, menu_item_id, step_id, batch_no)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_session_task_session_id | False | (session_id) |
| ix_session_task_menu_item_id | False | (menu_item_id) |
| ix_session_task_step_id | False | (step_id) |
| ix_session_task_search_0 | False | (session_id, planned_start_s) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_session_task_session_id | session_id | cooking_session(id) | CASCADE | RESTRICT | True |
| fk_session_task_menu_item_id | menu_item_id | menu_item(id) | CASCADE | RESTRICT | True |
| fk_session_task_step_id | step_id | recipe_step(id) | RESTRICT | RESTRICT | True |

保持・所属領域: owned / 献立

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| export_backup | R | backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q010_export_tables.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q100_delete_resource_reservation.sql |
| preview_backup | D | backend/src/app/apis/backup/preview_backup/sql/q100_delete_session_task.sql |
| preview_backup | R | backend/src/app/apis/backup/preview_backup/sql/q100_delete_task_dependency.sql |
| preview_backup | C | backend/src/app/apis/backup/preview_backup/sql/q200_insert_session_task.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q010_export_tables.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q100_delete_resource_reservation.sql |
| restore_backup | D | backend/src/app/apis/backup/restore_backup/sql/q100_delete_session_task.sql |
| restore_backup | R | backend/src/app/apis/backup/restore_backup/sql/q100_delete_task_dependency.sql |
| restore_backup | C | backend/src/app/apis/backup/restore_backup/sql/q200_insert_session_task.sql |
| entity_resource_reservation_create | R | backend/src/app/apis/entities/resource_reservation_create/sql/002_reference_task_id.sql |
| entity_resource_reservation_delete | R | backend/src/app/apis/entities/resource_reservation_delete/sql/001_delete.sql |
| entity_resource_reservation_get | R | backend/src/app/apis/entities/resource_reservation_get/sql/001_get.sql |
| entity_resource_reservation_list | R | backend/src/app/apis/entities/resource_reservation_list/sql/001_list.sql |
| entity_resource_reservation_update | R | backend/src/app/apis/entities/resource_reservation_update/sql/001_update.sql |
| entity_resource_reservation_update | R | backend/src/app/apis/entities/resource_reservation_update/sql/002_reference_task_id.sql |
| entity_session_task_create | C | backend/src/app/apis/entities/session_task_create/sql/001_create.sql |
| entity_session_task_delete | D | backend/src/app/apis/entities/session_task_delete/sql/001_delete.sql |
| entity_session_task_get | R | backend/src/app/apis/entities/session_task_get/sql/001_get.sql |
| entity_session_task_list | R | backend/src/app/apis/entities/session_task_list/sql/001_list.sql |
| entity_session_task_update | U | backend/src/app/apis/entities/session_task_update/sql/001_update.sql |
| entity_task_dependency_create | R | backend/src/app/apis/entities/task_dependency_create/sql/002_reference_before_task_id.sql |
| entity_task_dependency_create | R | backend/src/app/apis/entities/task_dependency_create/sql/003_reference_after_task_id.sql |
| entity_task_dependency_delete | R | backend/src/app/apis/entities/task_dependency_delete/sql/001_delete.sql |
| entity_task_dependency_get | R | backend/src/app/apis/entities/task_dependency_get/sql/001_get.sql |
| entity_task_dependency_list | R | backend/src/app/apis/entities/task_dependency_list/sql/001_list.sql |
| entity_task_dependency_update | R | backend/src/app/apis/entities/task_dependency_update/sql/001_update.sql |
| entity_task_dependency_update | R | backend/src/app/apis/entities/task_dependency_update/sql/002_reference_before_task_id.sql |
| entity_task_dependency_update | R | backend/src/app/apis/entities/task_dependency_update/sql/003_reference_after_task_id.sql |
| create_cooking_session | C | backend/src/app/apis/workspace/create_cooking_session/sql/q026_task.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/update_cooking_session/sql/q002_tasks.sql |
| update_cooking_session | U | backend/src/app/apis/workspace/update_cooking_session/sql/q004_complete_task.sql |
| update_cooking_session | U | backend/src/app/apis/workspace/update_cooking_session/sql/q005_timer.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| restore_backup | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql |
