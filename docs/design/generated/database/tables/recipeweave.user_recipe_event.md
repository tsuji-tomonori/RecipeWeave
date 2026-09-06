# テーブル仕様: recipeweave.user_recipe_event

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

提案・調理履歴

定義元: `database/migrations/002_relational_schema.sql:statement-462`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| user_id | uuid | 不可 | なし | なし | 利用者 |
| recipe_version_id | uuid | 不可 | なし | なし | 提案版 |
| kind | text | 不可 | なし | LENGTH(BTRIM(kind)) BETWEEN 1 AND 20000; kind IN ('shown', 'cooked', 'liked', 'disliked') | 提示/調理/評価 |
| occurred_at | timestamptz | 不可 | なし | なし | 発生時刻 |
| request_key | text | 不可 | なし | LENGTH(BTRIM(request_key)) BETWEEN 1 AND 20000 | リクエスト識別子 |

## 表制約

- `CHECK (LENGTH(BTRIM(kind)) BETWEEN 1 AND 20000)`
- `CHECK (kind IN ('shown', 'cooked', 'liked', 'disliked'))`
- `CHECK (LENGTH(BTRIM(request_key)) BETWEEN 1 AND 20000)`
- `UNIQUE (user_id, request_key, recipe_version_id, kind)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_user_recipe_event_user_id | False | (user_id) |
| ix_user_recipe_event_recipe_version_id | False | ( recipe_version_id ) |
| ix_user_recipe_event_search_0 | False | ( user_id, kind, occurred_at DESC ) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_user_recipe_event_user_id | user_id | app_user(id) | CASCADE | RESTRICT | True |
| fk_user_recipe_event_recipe_version_id | recipe_version_id | recipe_version(id) | RESTRICT | RESTRICT | True |

保持・所属領域: owned / 利用者

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_menu_item_create | R | backend/src/app/apis/entities/menu_item_create/sql/003_reference_recipe_version_id.sql |
| entity_menu_item_update | R | backend/src/app/apis/entities/menu_item_update/sql/003_reference_recipe_version_id.sql |
| entity_user_recipe_event_create | C | backend/src/app/apis/entities/user_recipe_event_create/sql/001_create.sql |
| entity_user_recipe_event_create | R | backend/src/app/apis/entities/user_recipe_event_create/sql/003_reference_recipe_version_id.sql |
| entity_user_recipe_event_delete | D | backend/src/app/apis/entities/user_recipe_event_delete/sql/001_delete.sql |
| entity_user_recipe_event_get | R | backend/src/app/apis/entities/user_recipe_event_get/sql/001_get.sql |
| entity_user_recipe_event_list | R | backend/src/app/apis/entities/user_recipe_event_list/sql/001_list.sql |
| get_recipe | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| save_recipe | C | backend/src/app/apis/workspace/save_recipe/sql/q002_event.sql |
| unsave_recipe | C | backend/src/app/apis/workspace/unsave_recipe/sql/q002_event.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| preview_cooking_plan | R | backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql |
