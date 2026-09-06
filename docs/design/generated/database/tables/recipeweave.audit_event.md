# テーブル仕様: recipeweave.audit_event

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

変更・公開監査

定義元: `database/migrations/002_relational_schema.sql:statement-582`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| actor_id | uuid | 可 | なし | なし | 実行者（削除時匿名化） |
| action | text | 不可 | なし | LENGTH(BTRIM(action)) BETWEEN 1 AND 20000 | publish/withdraw/erase等 |
| entity_type | text | 不可 | なし | LENGTH(BTRIM(entity_type)) BETWEEN 1 AND 20000 | 対象テーブルの許可リスト |
| entity_key_hash | char(64) | 不可 | なし | entity_key_hash IS NULL OR entity_key_hash ~ '^[0-9a-f]{64}$' | 対象識別子のハッシュ |
| reason | text | 不可 | なし | LENGTH(BTRIM(reason)) BETWEEN 1 AND 20000 | 理由（個人情報を含めない） |
| occurred_at | timestamptz | 不可 | なし | なし | 時刻 |

## 表制約

- `CHECK (LENGTH(BTRIM(action)) BETWEEN 1 AND 20000)`
- `CHECK (LENGTH(BTRIM(entity_type)) BETWEEN 1 AND 20000)`
- `CHECK (entity_key_hash IS NULL OR entity_key_hash ~ '^[0-9a-f]{64}$')`
- `CHECK (LENGTH(BTRIM(reason)) BETWEEN 1 AND 20000)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_audit_event_actor_id | False | (actor_id) |
| ix_audit_event_search_0 | False | (occurred_at) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_audit_event_actor_id | actor_id | app_user(id) | SET NULL | RESTRICT | True |

保持・所属領域: audit / 運用

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| restore_backup | C | backend/src/app/apis/backup/restore_backup/sql/q902_append_audit.sql |
| entity_audit_event_get | R | backend/src/app/apis/entities/audit_event_get/sql/001_get.sql |
| entity_audit_event_list | R | backend/src/app/apis/entities/audit_event_list/sql/001_list.sql |
| add_menu_item | C | backend/src/app/apis/workspace/add_menu_item/sql/q902_append_audit.sql |
| commit_receipt | C | backend/src/app/apis/workspace/commit_receipt/sql/q902_append_audit.sql |
| create_cooking_session | C | backend/src/app/apis/workspace/create_cooking_session/sql/q902_append_audit.sql |
| create_custom_food | C | backend/src/app/apis/workspace/create_custom_food/sql/q902_append_audit.sql |
| create_pantry_lot | C | backend/src/app/apis/workspace/create_pantry_lot/sql/q902_append_audit.sql |
| delete_menu_item | C | backend/src/app/apis/workspace/delete_menu_item/sql/q902_append_audit.sql |
| delete_pantry_lot | C | backend/src/app/apis/workspace/delete_pantry_lot/sql/q902_append_audit.sql |
| put_settings | C | backend/src/app/apis/workspace/put_settings/sql/q902_append_audit.sql |
| put_shopping_checks | C | backend/src/app/apis/workspace/put_shopping_checks/sql/q902_append_audit.sql |
| save_recipe | C | backend/src/app/apis/workspace/save_recipe/sql/q902_append_audit.sql |
| undo_receipt | C | backend/src/app/apis/workspace/undo_receipt/sql/q902_append_audit.sql |
| unsave_recipe | C | backend/src/app/apis/workspace/unsave_recipe/sql/q902_append_audit.sql |
| update_cooking_session | C | backend/src/app/apis/workspace/update_cooking_session/sql/q902_append_audit.sql |
| update_menu_item | C | backend/src/app/apis/workspace/update_menu_item/sql/q902_append_audit.sql |
| update_pantry_lot | C | backend/src/app/apis/workspace/update_pantry_lot/sql/q902_append_audit.sql |
| entity_source_record_create | C | backend/src/app/entities/sql/audit.sql |
| entity_source_record_update | C | backend/src/app/entities/sql/audit.sql |
| entity_catalog_release_create | C | backend/src/app/entities/sql/audit.sql |
| entity_catalog_release_update | C | backend/src/app/entities/sql/audit.sql |
| entity_unit_create | C | backend/src/app/entities/sql/audit.sql |
| entity_unit_update | C | backend/src/app/entities/sql/audit.sql |
| entity_food_create | C | backend/src/app/entities/sql/audit.sql |
| entity_food_update | C | backend/src/app/entities/sql/audit.sql |
| entity_food_alias_create | C | backend/src/app/entities/sql/audit.sql |
| entity_food_alias_update | C | backend/src/app/entities/sql/audit.sql |
| entity_food_form_create | C | backend/src/app/entities/sql/audit.sql |
| entity_food_form_update | C | backend/src/app/entities/sql/audit.sql |
| entity_conversion_create | C | backend/src/app/entities/sql/audit.sql |
| entity_conversion_update | C | backend/src/app/entities/sql/audit.sql |
| entity_form_yield_create | C | backend/src/app/entities/sql/audit.sql |
| entity_product_create | C | backend/src/app/entities/sql/audit.sql |
| entity_product_update | C | backend/src/app/entities/sql/audit.sql |
| entity_product_version_create | C | backend/src/app/entities/sql/audit.sql |
| entity_product_component_create | C | backend/src/app/entities/sql/audit.sql |
| entity_allergen_create | C | backend/src/app/entities/sql/audit.sql |
| entity_allergen_update | C | backend/src/app/entities/sql/audit.sql |
| entity_food_allergen_create | C | backend/src/app/entities/sql/audit.sql |
| entity_product_allergen_create | C | backend/src/app/entities/sql/audit.sql |
| entity_nutrient_create | C | backend/src/app/entities/sql/audit.sql |
| entity_nutrient_update | C | backend/src/app/entities/sql/audit.sql |
| entity_nutrition_fact_create | C | backend/src/app/entities/sql/audit.sql |
| entity_axis_create | C | backend/src/app/entities/sql/audit.sql |
| entity_axis_update | C | backend/src/app/entities/sql/audit.sql |
| entity_axis_option_create | C | backend/src/app/entities/sql/audit.sql |
| entity_axis_option_update | C | backend/src/app/entities/sql/audit.sql |
| entity_food_axis_option_create | C | backend/src/app/entities/sql/audit.sql |
| entity_food_axis_option_update | C | backend/src/app/entities/sql/audit.sql |
| entity_recipe_create | C | backend/src/app/entities/sql/audit.sql |
| entity_recipe_update | C | backend/src/app/entities/sql/audit.sql |
| entity_recipe_version_create | C | backend/src/app/entities/sql/audit.sql |
| entity_recipe_version_update | C | backend/src/app/entities/sql/audit.sql |
| entity_recipe_option_create | C | backend/src/app/entities/sql/audit.sql |
| entity_recipe_option_update | C | backend/src/app/entities/sql/audit.sql |
| entity_scaling_rule_create | C | backend/src/app/entities/sql/audit.sql |
| entity_scaling_point_create | C | backend/src/app/entities/sql/audit.sql |
| entity_recipe_ingredient_create | C | backend/src/app/entities/sql/audit.sql |
| entity_recipe_ingredient_update | C | backend/src/app/entities/sql/audit.sql |
| entity_operation_create | C | backend/src/app/entities/sql/audit.sql |
| entity_operation_update | C | backend/src/app/entities/sql/audit.sql |
| entity_operation_parameter_create | C | backend/src/app/entities/sql/audit.sql |
| entity_operation_parameter_update | C | backend/src/app/entities/sql/audit.sql |
| entity_recipe_step_create | C | backend/src/app/entities/sql/audit.sql |
| entity_recipe_step_update | C | backend/src/app/entities/sql/audit.sql |
| entity_step_parameter_create | C | backend/src/app/entities/sql/audit.sql |
| entity_step_parameter_update | C | backend/src/app/entities/sql/audit.sql |
| entity_material_node_create | C | backend/src/app/entities/sql/audit.sql |
| entity_material_node_update | C | backend/src/app/entities/sql/audit.sql |
| entity_step_input_create | C | backend/src/app/entities/sql/audit.sql |
| entity_step_input_update | C | backend/src/app/entities/sql/audit.sql |
| entity_step_dependency_create | C | backend/src/app/entities/sql/audit.sql |
| entity_step_dependency_update | C | backend/src/app/entities/sql/audit.sql |
| entity_resource_type_create | C | backend/src/app/entities/sql/audit.sql |
| entity_resource_type_update | C | backend/src/app/entities/sql/audit.sql |
| entity_step_resource_create | C | backend/src/app/entities/sql/audit.sql |
| entity_step_resource_update | C | backend/src/app/entities/sql/audit.sql |
| entity_media_asset_create | C | backend/src/app/entities/sql/audit.sql |
| entity_step_media_create | C | backend/src/app/entities/sql/audit.sql |
| entity_step_media_update | C | backend/src/app/entities/sql/audit.sql |
| entity_generation_policy_create | C | backend/src/app/entities/sql/audit.sql |
| entity_generation_job_create | C | backend/src/app/entities/sql/audit.sql |
| entity_generation_job_update | C | backend/src/app/entities/sql/audit.sql |
| entity_generation_choice_create | C | backend/src/app/entities/sql/audit.sql |
| entity_generation_choice_update | C | backend/src/app/entities/sql/audit.sql |
| entity_generation_food_create | C | backend/src/app/entities/sql/audit.sql |
| entity_generation_food_update | C | backend/src/app/entities/sql/audit.sql |
| entity_generation_result_create | C | backend/src/app/entities/sql/audit.sql |
| entity_compatibility_rule_create | C | backend/src/app/entities/sql/audit.sql |
| entity_validation_result_create | C | backend/src/app/entities/sql/audit.sql |
| entity_recipe_signature_create | C | backend/src/app/entities/sql/audit.sql |
| entity_recipe_similarity_create | C | backend/src/app/entities/sql/audit.sql |
| entity_recipe_similarity_update | C | backend/src/app/entities/sql/audit.sql |
| entity_app_user_update | C | backend/src/app/entities/sql/audit.sql |
| entity_user_preference_create | C | backend/src/app/entities/sql/audit.sql |
| entity_user_preference_update | C | backend/src/app/entities/sql/audit.sql |
| entity_user_preference_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_user_exclusion_create | C | backend/src/app/entities/sql/audit.sql |
| entity_user_exclusion_update | C | backend/src/app/entities/sql/audit.sql |
| entity_user_exclusion_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_user_recipe_event_create | C | backend/src/app/entities/sql/audit.sql |
| entity_user_recipe_event_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_menu_create | C | backend/src/app/entities/sql/audit.sql |
| entity_menu_update | C | backend/src/app/entities/sql/audit.sql |
| entity_menu_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_menu_item_create | C | backend/src/app/entities/sql/audit.sql |
| entity_menu_item_update | C | backend/src/app/entities/sql/audit.sql |
| entity_menu_item_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_menu_ingredient_override_create | C | backend/src/app/entities/sql/audit.sql |
| entity_menu_ingredient_override_update | C | backend/src/app/entities/sql/audit.sql |
| entity_menu_ingredient_override_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_kitchen_resource_create | C | backend/src/app/entities/sql/audit.sql |
| entity_kitchen_resource_update | C | backend/src/app/entities/sql/audit.sql |
| entity_kitchen_resource_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_cooking_session_create | C | backend/src/app/entities/sql/audit.sql |
| entity_cooking_session_update | C | backend/src/app/entities/sql/audit.sql |
| entity_cooking_session_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_session_task_create | C | backend/src/app/entities/sql/audit.sql |
| entity_session_task_update | C | backend/src/app/entities/sql/audit.sql |
| entity_session_task_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_task_dependency_create | C | backend/src/app/entities/sql/audit.sql |
| entity_task_dependency_update | C | backend/src/app/entities/sql/audit.sql |
| entity_task_dependency_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_resource_reservation_create | C | backend/src/app/entities/sql/audit.sql |
| entity_resource_reservation_update | C | backend/src/app/entities/sql/audit.sql |
| entity_resource_reservation_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_pantry_lot_create | C | backend/src/app/entities/sql/audit.sql |
| entity_pantry_lot_update | C | backend/src/app/entities/sql/audit.sql |
| entity_pantry_lot_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_shopping_item_create | C | backend/src/app/entities/sql/audit.sql |
| entity_shopping_item_update | C | backend/src/app/entities/sql/audit.sql |
| entity_shopping_item_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_product_preparation_rule_create | C | backend/src/app/entities/sql/audit.sql |
| entity_food_identity_create | C | backend/src/app/entities/sql/audit.sql |
| entity_food_identity_member_create | C | backend/src/app/entities/sql/audit.sql |
| entity_generation_template_create | C | backend/src/app/entities/sql/audit.sql |
| entity_generation_shard_create | C | backend/src/app/entities/sql/audit.sql |
| entity_candidate_attempt_create | C | backend/src/app/entities/sql/audit.sql |
| entity_candidate_attempt_update | C | backend/src/app/entities/sql/audit.sql |
| entity_recipe_embedding_create | C | backend/src/app/entities/sql/audit.sql |
| entity_recipe_embedding_update | C | backend/src/app/entities/sql/audit.sql |
| entity_generation_stratum_metric_create | C | backend/src/app/entities/sql/audit.sql |
| entity_receipt_import_create | C | backend/src/app/entities/sql/audit.sql |
| entity_receipt_import_update | C | backend/src/app/entities/sql/audit.sql |
| entity_receipt_import_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_receipt_line_create | C | backend/src/app/entities/sql/audit.sql |
| entity_receipt_line_update | C | backend/src/app/entities/sql/audit.sql |
| entity_receipt_line_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_user_food_create | C | backend/src/app/entities/sql/audit.sql |
| entity_user_food_update | C | backend/src/app/entities/sql/audit.sql |
| entity_user_food_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_user_pantry_food_create | C | backend/src/app/entities/sql/audit.sql |
| entity_user_pantry_food_update | C | backend/src/app/entities/sql/audit.sql |
| entity_user_pantry_food_delete | C | backend/src/app/entities/sql/audit.sql |
| entity_user_shopping_check_create | C | backend/src/app/entities/sql/audit.sql |
| entity_user_shopping_check_update | C | backend/src/app/entities/sql/audit.sql |
| entity_user_shopping_check_delete | C | backend/src/app/entities/sql/audit.sql |
| advance_shard | C | backend/src/app/entities/sql/audit.sql |
| claim_shard | C | backend/src/app/entities/sql/audit.sql |
| renew_shard | C | backend/src/app/entities/sql/audit.sql |
