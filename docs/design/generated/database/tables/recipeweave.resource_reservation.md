# テーブル仕様: recipeweave.resource_reservation

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

資源の予約

定義元: `database/migrations/002_relational_schema.sql:statement-540`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| task_id | uuid | 不可 | なし | なし | 使用タスク |
| resource_id | uuid | 不可 | なし | なし | 実資源 |
| start_s | integer | 不可 | なし | start_s &gt;= 0; end_s &gt; start_s | 占有開始 |
| end_s | integer | 不可 | なし | end_s &gt; start_s | 占有終了 |
| quantity | integer | 不可 | なし | quantity &gt; 0 | 占有量 |

## 表制約

- `CHECK (start_s >= 0)`
- `CHECK (end_s > start_s)`
- `CHECK (quantity > 0)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_resource_reservation_task_id | False | (task_id) |
| ix_resource_reservation_resource_id | False | (resource_id) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_resource_reservation_task_id | task_id | session_task(id) | CASCADE | RESTRICT | True |
| fk_resource_reservation_resource_id | resource_id | kitchen_resource(id) | RESTRICT | RESTRICT | True |

保持・所属領域: owned / 献立

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_resource_reservation_create | C | backend/src/app/apis/entities/resource_reservation_create/sql/001_create.sql |
| entity_resource_reservation_delete | D | backend/src/app/apis/entities/resource_reservation_delete/sql/001_delete.sql |
| entity_resource_reservation_get | R | backend/src/app/apis/entities/resource_reservation_get/sql/001_get.sql |
| entity_resource_reservation_list | R | backend/src/app/apis/entities/resource_reservation_list/sql/001_list.sql |
| entity_resource_reservation_update | U | backend/src/app/apis/entities/resource_reservation_update/sql/001_update.sql |
| create_cooking_session | C | backend/src/app/apis/workspace/create_cooking_session/sql/q028_reservation.sql |
