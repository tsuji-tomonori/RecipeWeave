# テーブル仕様: recipeweave.kitchen_resource

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

キッチンの実資源

定義元: `database/migrations/002_relational_schema.sql:statement-498`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| user_id | uuid | 不可 | なし | なし | 所有者 |
| resource_type_id | uuid | 不可 | なし | なし | コンロ・鍋・人等 |
| name | text | 不可 | なし | LENGTH(BTRIM(name)) BETWEEN 1 AND 20000 | 左コンロ・26cmフライパン等 |
| capacity | numeric(20,6) | 可 | なし | capacity IS NULL OR capacity &gt; 0; capacity IS NULL OR capacity::TEXT NOT IN ('NaN', 'Infinity', '-Infinity') | 容量 |
| quantity | integer | 不可 | なし | quantity &gt; 0 | 同等資源数 |
| active | boolean | 不可 | TRUE | なし | 新規の調理計画で利用する資源か |

## 表制約

- `CHECK (quantity > 0)`
- `CHECK (capacity IS NULL OR capacity > 0)`
- `CHECK (LENGTH(BTRIM(name)) BETWEEN 1 AND 20000)`
- `CHECK (capacity IS NULL OR capacity::TEXT NOT IN ('NaN', 'Infinity', '-Infinity'))`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_kitchen_resource_user_id | False | (user_id) |
| ix_kitchen_resource_resource_type_id | False | ( resource_type_id ) |

## 外部キー

| 名称 | 列 | 参照先 | 削除 | 更新 | 遅延検査 |
|---|---|---|---|---|---|
| fk_kitchen_resource_user_id | user_id | app_user(id) | CASCADE | RESTRICT | True |
| fk_kitchen_resource_resource_type_id | resource_type_id | resource_type(id) | RESTRICT | RESTRICT | True |

保持・所属領域: owned / 献立

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| get_me | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_kitchen_resource_create | C | backend/src/app/apis/entities/kitchen_resource_create/sql/001_create.sql |
| entity_kitchen_resource_delete | D | backend/src/app/apis/entities/kitchen_resource_delete/sql/001_delete.sql |
| entity_kitchen_resource_get | R | backend/src/app/apis/entities/kitchen_resource_get/sql/001_get.sql |
| entity_kitchen_resource_list | R | backend/src/app/apis/entities/kitchen_resource_list/sql/001_list.sql |
| entity_kitchen_resource_update | U | backend/src/app/apis/entities/kitchen_resource_update/sql/001_update.sql |
| entity_resource_reservation_create | R | backend/src/app/apis/entities/resource_reservation_create/sql/003_reference_resource_id.sql |
| entity_resource_reservation_update | R | backend/src/app/apis/entities/resource_reservation_update/sql/003_reference_resource_id.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/create_cooking_session/sql/q023_resources.sql |
| get_workspace | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| preview_cooking_plan | R | backend/src/app/apis/workspace/preview_cooking_plan/sql/q004_resources.sql |
| put_settings | U | backend/src/app/apis/workspace/put_settings/sql/q003_clear_equipment.sql |
| put_settings | U | backend/src/app/apis/workspace/put_settings/sql/q006_equipment.sql |
| put_settings | C,R | backend/src/app/apis/workspace/put_settings/sql/q007_add_equipment.sql |
| add_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| commit_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| create_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| create_custom_food | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| create_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| delete_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| delete_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| put_settings | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| put_shopping_checks | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| save_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| undo_receipt | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| unsave_recipe | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| update_cooking_session | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| update_menu_item | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| update_pantry_lot | R | backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql |
| entity_allergen_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_allergen_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_allergen_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_allergen_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_app_user_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_app_user_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_app_user_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_audit_event_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_audit_event_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_axis_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_axis_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_axis_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_axis_option_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_axis_option_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_axis_option_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_axis_option_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_axis_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_candidate_attempt_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_candidate_attempt_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_candidate_attempt_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_candidate_attempt_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_catalog_release_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_catalog_release_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_catalog_release_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_catalog_release_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_compatibility_rule_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_compatibility_rule_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_compatibility_rule_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_conversion_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_conversion_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_conversion_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_conversion_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_cooking_session_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_cooking_session_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_cooking_session_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_cooking_session_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_cooking_session_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_alias_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_alias_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_alias_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_alias_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_allergen_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_allergen_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_allergen_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_axis_option_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_axis_option_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_axis_option_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_axis_option_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_form_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_form_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_form_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_form_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_identity_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_identity_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_identity_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_identity_member_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_identity_member_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_identity_member_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_food_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_form_yield_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_form_yield_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_form_yield_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_choice_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_choice_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_choice_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_choice_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_food_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_food_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_food_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_food_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_job_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_job_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_job_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_job_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_policy_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_policy_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_policy_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_result_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_result_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_result_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_shard_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_shard_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_shard_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_stratum_metric_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_stratum_metric_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_stratum_metric_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_template_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_template_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_generation_template_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_ingredient_total_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_ingredient_total_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_kitchen_resource_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_kitchen_resource_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_kitchen_resource_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_kitchen_resource_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_kitchen_resource_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_material_node_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_material_node_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_material_node_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_material_node_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_media_asset_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_media_asset_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_media_asset_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_menu_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_menu_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_menu_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_menu_ingredient_override_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_menu_ingredient_override_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_menu_ingredient_override_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_menu_ingredient_override_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_menu_ingredient_override_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_menu_item_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_menu_item_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_menu_item_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_menu_item_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_menu_item_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_menu_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_menu_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_nutrient_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_nutrient_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_nutrient_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_nutrient_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_nutrition_fact_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_nutrition_fact_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_nutrition_fact_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_operation_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_operation_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_operation_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_operation_parameter_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_operation_parameter_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_operation_parameter_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_operation_parameter_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_operation_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_outbox_event_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_outbox_event_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_pantry_consumption_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_pantry_consumption_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_pantry_lot_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_pantry_lot_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_pantry_lot_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_pantry_lot_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_pantry_lot_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_product_allergen_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_product_allergen_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_product_allergen_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_product_component_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_product_component_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_product_component_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_product_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_product_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_product_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_product_preparation_rule_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_product_preparation_rule_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_product_preparation_rule_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_product_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_product_version_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_product_version_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_product_version_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_receipt_import_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_receipt_import_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_receipt_import_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_receipt_import_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_receipt_import_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_receipt_line_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_receipt_line_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_receipt_line_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_receipt_line_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_receipt_line_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_embedding_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_embedding_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_embedding_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_embedding_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_ingredient_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_ingredient_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_ingredient_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_ingredient_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_option_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_option_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_option_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_option_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_search_document_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_search_document_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_signature_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_signature_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_signature_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_similarity_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_similarity_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_similarity_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_similarity_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_step_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_step_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_step_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_step_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_version_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_version_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_version_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_recipe_version_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_resource_reservation_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_resource_reservation_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_resource_reservation_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_resource_reservation_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_resource_reservation_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_resource_type_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_resource_type_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_resource_type_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_resource_type_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_scaling_point_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_scaling_point_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_scaling_point_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_scaling_rule_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_scaling_rule_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_scaling_rule_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_session_task_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_session_task_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_session_task_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_session_task_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_session_task_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_shopping_item_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_shopping_item_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_shopping_item_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_shopping_item_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_shopping_item_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_source_record_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_source_record_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_source_record_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_source_record_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_dependency_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_dependency_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_dependency_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_dependency_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_input_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_input_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_input_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_input_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_media_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_media_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_media_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_media_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_parameter_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_parameter_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_parameter_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_parameter_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_resource_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_resource_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_resource_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_step_resource_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_task_dependency_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_task_dependency_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_task_dependency_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_task_dependency_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_task_dependency_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_unit_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_unit_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_unit_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_unit_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_exclusion_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_exclusion_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_exclusion_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_exclusion_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_exclusion_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_food_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_food_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_food_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_food_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_food_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_pantry_food_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_pantry_food_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_pantry_food_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_pantry_food_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_pantry_food_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_preference_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_preference_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_preference_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_preference_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_preference_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_recipe_event_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_recipe_event_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_recipe_event_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_recipe_event_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_shopping_check_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_shopping_check_delete | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_shopping_check_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_shopping_check_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_user_shopping_check_update | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_validation_result_create | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_validation_result_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_validation_result_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_workspace_revision_get | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| entity_workspace_revision_list | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| advance_shard | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| claim_shard | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| renew_shard | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| get_recipe | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| list_recipes | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| random_recipe | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| add_menu_item | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| commit_receipt | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| create_cooking_session | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| create_custom_food | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| create_pantry_lot | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| delete_menu_item | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| delete_pantry_lot | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| get_workspace | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| preview_cooking_plan | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| put_settings | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| put_shopping_checks | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| save_recipe | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| undo_receipt | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| unsave_recipe | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| update_cooking_session | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| update_menu_item | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
| update_pantry_lot | C,R | backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql |
