# 物理ER図

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

```mermaid
erDiagram
    recipeweave_allergen {
        uuid id PK
        timestamptz created_at
        text code
        text name
        uuid source_id
    }
    recipeweave_source_record |o--o{ recipeweave_allergen : "source_id"
    recipeweave_app_user {
        uuid id PK
        timestamptz created_at
        text auth_subject
        text state
        text locale
        text timezone
    }
    recipeweave_audit_event {
        uuid id PK
        timestamptz created_at
        uuid actor_id
        text action
        text entity_type
        char_64_ entity_key_hash
        text reason
        timestamptz occurred_at
    }
    recipeweave_app_user |o--o{ recipeweave_audit_event : "actor_id"
    recipeweave_axis {
        uuid id PK
        timestamptz created_at
        text code
        text name
        text purpose
        text selection
        uuid release_id
        text status
    }
    recipeweave_catalog_release ||--o{ recipeweave_axis : "release_id"
    recipeweave_axis_option {
        uuid id PK
        timestamptz created_at
        uuid axis_id
        text code
        text label
        text definition
        uuid parent_id
        text status
    }
    recipeweave_axis ||--o{ recipeweave_axis_option : "axis_id"
    recipeweave_axis_option |o--o{ recipeweave_axis_option : "parent_id"
    recipeweave_candidate_attempt {
        uuid id PK
        timestamptz created_at
        uuid template_id
        bigint ordinal
        char_64_ design_key
        uuid job_id
        text state
        text reason_code
        uuid recipe_version_id
        integer attempts
    }
    recipeweave_generation_template ||--o{ recipeweave_candidate_attempt : "template_id"
    recipeweave_generation_job |o--o{ recipeweave_candidate_attempt : "job_id"
    recipeweave_recipe_version |o--o{ recipeweave_candidate_attempt : "recipe_version_id"
    recipeweave_catalog_release {
        uuid id PK
        timestamptz created_at
        text version
        char_64_ manifest_hash
        timestamptz published_at
        uuid owner_id
    }
    recipeweave_app_user |o--o{ recipeweave_catalog_release : "owner_id"
    recipeweave_compatibility_rule {
        uuid id PK
        timestamptz created_at
        text code
        integer version
        text severity
        jsonb predicate
        text message
        uuid source_id
        text status
    }
    recipeweave_source_record |o--o{ recipeweave_compatibility_rule : "source_id"
    recipeweave_conversion {
        uuid id PK
        timestamptz created_at
        uuid form_id
        uuid from_unit_id
        uuid to_unit_id
        numeric_20_6_ factor
        text quality
        uuid source_id
        text conditions
        uuid release_id
    }
    recipeweave_food_form ||--o{ recipeweave_conversion : "form_id"
    recipeweave_unit ||--o{ recipeweave_conversion : "from_unit_id"
    recipeweave_unit ||--o{ recipeweave_conversion : "to_unit_id"
    recipeweave_source_record |o--o{ recipeweave_conversion : "source_id"
    recipeweave_catalog_release ||--o{ recipeweave_conversion : "release_id"
    recipeweave_cooking_session {
        uuid id PK
        timestamptz created_at
        uuid menu_id
        integer menu_revision
        text status
        timestamptz target_at
        text planner_version
        jsonb input_snapshot
        char_64_ input_hash
        integer current_task_index
    }
    recipeweave_menu ||--o{ recipeweave_cooking_session : "menu_id"
    recipeweave_food {
        uuid id PK
        timestamptz created_at
        text code
        text name
        text kind
        uuid parent_id
        uuid release_id
        text status
        uuid owner_id
    }
    recipeweave_food |o--o{ recipeweave_food : "parent_id"
    recipeweave_catalog_release ||--o{ recipeweave_food : "release_id"
    recipeweave_app_user |o--o{ recipeweave_food : "owner_id"
    recipeweave_food_alias {
        uuid id PK
        timestamptz created_at
        uuid food_id
        text alias
        text locale
    }
    recipeweave_food ||--o{ recipeweave_food_alias : "food_id"
    recipeweave_food_allergen {
        uuid id PK
        timestamptz created_at
        uuid form_id
        uuid allergen_id
        text presence
        uuid source_id
    }
    recipeweave_food_form ||--o{ recipeweave_food_allergen : "form_id"
    recipeweave_allergen ||--o{ recipeweave_food_allergen : "allergen_id"
    recipeweave_source_record ||--o{ recipeweave_food_allergen : "source_id"
    recipeweave_food_axis_option {
        uuid id PK
        timestamptz created_at
        uuid food_id
        uuid option_id
    }
    recipeweave_food ||--o{ recipeweave_food_axis_option : "food_id"
    recipeweave_axis_option ||--o{ recipeweave_food_axis_option : "option_id"
    recipeweave_food_form {
        uuid id PK
        timestamptz created_at
        uuid food_id
        text name
        text state
        uuid base_unit_id
        text quantity_basis
        text status
    }
    recipeweave_food ||--o{ recipeweave_food_form : "food_id"
    recipeweave_unit ||--o{ recipeweave_food_form : "base_unit_id"
    recipeweave_food_identity {
        uuid id PK
        timestamptz created_at
        text code
        text name
        text normalizer_version
    }
    recipeweave_food_identity_member {
        uuid id PK
        timestamptz created_at
        uuid food_id
        uuid identity_id
        text normalizer_version
        text reason
    }
    recipeweave_food ||--o{ recipeweave_food_identity_member : "food_id"
    recipeweave_food_identity ||--o{ recipeweave_food_identity_member : "identity_id"
    recipeweave_form_yield {
        uuid id PK
        timestamptz created_at
        uuid input_form_id
        uuid output_form_id
        numeric_20_6_ yield_ratio
        uuid source_id
        text quality
        text conditions
    }
    recipeweave_food_form ||--o{ recipeweave_form_yield : "input_form_id"
    recipeweave_food_form ||--o{ recipeweave_form_yield : "output_form_id"
    recipeweave_source_record |o--o{ recipeweave_form_yield : "source_id"
    recipeweave_generation_choice {
        uuid id PK
        timestamptz created_at
        uuid job_id
        uuid option_id
    }
    recipeweave_generation_job ||--o{ recipeweave_generation_choice : "job_id"
    recipeweave_axis_option ||--o{ recipeweave_generation_choice : "option_id"
    recipeweave_generation_food {
        uuid id PK
        timestamptz created_at
        uuid job_id
        uuid form_id
        text role
    }
    recipeweave_generation_job ||--o{ recipeweave_generation_food : "job_id"
    recipeweave_food_form ||--o{ recipeweave_generation_food : "form_id"
    recipeweave_generation_job {
        uuid id PK
        timestamptz created_at
        uuid policy_id
        char_64_ idempotency_key
        text status
        timestamptz started_at
        timestamptz finished_at
        integer seed
        text error_code
        integer attempt_count
    }
    recipeweave_generation_policy ||--o{ recipeweave_generation_job : "policy_id"
    recipeweave_generation_policy {
        uuid id PK
        timestamptz created_at
        text version
        text prompt_template
        text model_identifier
        jsonb parameter_json
        text schema_version
        uuid release_id
    }
    recipeweave_catalog_release ||--o{ recipeweave_generation_policy : "release_id"
    recipeweave_generation_result {
        uuid id PK
        timestamptz created_at
        uuid recipe_version_id
        uuid job_id
        uuid policy_id
        jsonb input_snapshot
        text raw_output_uri
        char_64_ raw_output_hash
    }
    recipeweave_recipe_version ||--o| recipeweave_generation_result : "recipe_version_id"
    recipeweave_generation_job |o--o{ recipeweave_generation_result : "job_id"
    recipeweave_generation_policy ||--o{ recipeweave_generation_result : "policy_id"
    recipeweave_generation_shard {
        uuid id PK
        timestamptz created_at
        uuid template_id
        bigint start_ordinal
        bigint end_ordinal
        bigint next_ordinal
        text lease_owner
        timestamptz lease_expires_at
        bigint fence_token
        text state
    }
    recipeweave_generation_template ||--o{ recipeweave_generation_shard : "template_id"
    recipeweave_generation_stratum_metric {
        uuid id PK
        timestamptz created_at
        uuid template_id
        timestamptz window_start
        timestamptz window_end
        bigint attempted
        bigint valid
        bigint unique_count
        bigint publishable
        bigint input_tokens
        bigint output_tokens
        numeric_20_6_ cost_amount
        char_3_ currency
        text stratum_key
    }
    recipeweave_generation_template ||--o{ recipeweave_generation_stratum_metric : "template_id"
    recipeweave_generation_template {
        uuid id PK
        timestamptz created_at
        text code
        integer version
        uuid release_id
        jsonb contract
        bigint candidate_count
        char_64_ contract_hash
    }
    recipeweave_catalog_release ||--o{ recipeweave_generation_template : "release_id"
    recipeweave_ingredient_total {
        uuid id PK
        timestamptz created_at
        uuid session_id
        uuid form_id
        uuid product_version_id
        uuid unit_id
        numeric_20_6_ required_amount
        text quality
        text calculation_version
        numeric_20_6_ actual_amount
        text consumption_outcome
    }
    recipeweave_cooking_session ||--o{ recipeweave_ingredient_total : "session_id"
    recipeweave_food_form ||--o{ recipeweave_ingredient_total : "form_id"
    recipeweave_product_version |o--o{ recipeweave_ingredient_total : "product_version_id"
    recipeweave_unit ||--o{ recipeweave_ingredient_total : "unit_id"
    recipeweave_kitchen_resource {
        uuid id PK
        timestamptz created_at
        uuid user_id
        uuid resource_type_id
        text name
        numeric_20_6_ capacity
        integer quantity
        boolean active
    }
    recipeweave_app_user ||--o{ recipeweave_kitchen_resource : "user_id"
    recipeweave_resource_type ||--o{ recipeweave_kitchen_resource : "resource_type_id"
    recipeweave_material_node {
        uuid id PK
        timestamptz created_at
        uuid recipe_version_id
        text name
        text kind
        uuid ingredient_line_id
        uuid producer_step_id
        numeric_20_6_ amount
        uuid unit_id
    }
    recipeweave_recipe_version ||--o{ recipeweave_material_node : "recipe_version_id"
    recipeweave_recipe_ingredient |o--o{ recipeweave_material_node : "ingredient_line_id"
    recipeweave_recipe_step |o--o{ recipeweave_material_node : "producer_step_id"
    recipeweave_unit |o--o{ recipeweave_material_node : "unit_id"
    recipeweave_media_asset {
        uuid id PK
        timestamptz created_at
        uuid operation_id
        text media_type
        text uri
        char_64_ sha256
        text locale
        integer version
        jsonb parameter_contract
        uuid source_id
        text validation
    }
    recipeweave_operation ||--o{ recipeweave_media_asset : "operation_id"
    recipeweave_source_record ||--o{ recipeweave_media_asset : "source_id"
    recipeweave_menu {
        uuid id PK
        timestamptz created_at
        uuid user_id
        text name
        numeric_20_6_ servings
        integer revision
    }
    recipeweave_app_user ||--o{ recipeweave_menu : "user_id"
    recipeweave_menu_ingredient_override {
        uuid id PK
        timestamptz created_at
        uuid menu_item_id
        uuid ingredient_line_id
        boolean selected
        numeric_20_6_ amount
        uuid form_id
        uuid product_version_id
    }
    recipeweave_menu_item ||--o{ recipeweave_menu_ingredient_override : "menu_item_id"
    recipeweave_recipe_ingredient ||--o{ recipeweave_menu_ingredient_override : "ingredient_line_id"
    recipeweave_food_form |o--o{ recipeweave_menu_ingredient_override : "form_id"
    recipeweave_product_version |o--o{ recipeweave_menu_ingredient_override : "product_version_id"
    recipeweave_menu_item {
        uuid id PK
        timestamptz created_at
        uuid menu_id
        uuid recipe_version_id
        numeric_20_6_ servings
        uuid role_option_id
        integer position
    }
    recipeweave_menu ||--o{ recipeweave_menu_item : "menu_id"
    recipeweave_recipe_version ||--o{ recipeweave_menu_item : "recipe_version_id"
    recipeweave_axis_option ||--o{ recipeweave_menu_item : "role_option_id"
    recipeweave_nutrient {
        uuid id PK
        timestamptz created_at
        text code
        text name
        text unit_label
    }
    recipeweave_nutrition_fact {
        uuid id PK
        timestamptz created_at
        uuid form_id
        uuid product_version_id
        uuid nutrient_id
        numeric_20_6_ amount
        numeric_20_6_ basis_amount
        uuid basis_unit_id
        uuid source_id
    }
    recipeweave_food_form |o--o{ recipeweave_nutrition_fact : "form_id"
    recipeweave_product_version |o--o{ recipeweave_nutrition_fact : "product_version_id"
    recipeweave_nutrient ||--o{ recipeweave_nutrition_fact : "nutrient_id"
    recipeweave_unit ||--o{ recipeweave_nutrition_fact : "basis_unit_id"
    recipeweave_source_record ||--o{ recipeweave_nutrition_fact : "source_id"
    recipeweave_operation {
        uuid id PK
        timestamptz created_at
        text code
        text name
        text definition
        text precondition
        text completion_cue
        text status
    }
    recipeweave_operation_parameter {
        uuid id PK
        timestamptz created_at
        uuid operation_id
        text code
        text name
        text value_type
        uuid unit_id
        boolean required
        numeric_20_6_ min_value
        numeric_20_6_ max_value
        jsonb allowed_values
    }
    recipeweave_operation ||--o{ recipeweave_operation_parameter : "operation_id"
    recipeweave_unit |o--o{ recipeweave_operation_parameter : "unit_id"
    recipeweave_outbox_event {
        uuid id PK
        timestamptz created_at
        text event_type
        uuid aggregate_id
        jsonb payload
        timestamptz delivered_at
        integer attempt_count
    }
    recipeweave_pantry_consumption {
        uuid id PK
        timestamptz created_at
        uuid user_id
        uuid session_id
        uuid lot_id
        numeric_20_6_ amount
        uuid unit_id
    }
    recipeweave_app_user ||--o{ recipeweave_pantry_consumption : "user_id"
    recipeweave_cooking_session ||--o{ recipeweave_pantry_consumption : "session_id"
    recipeweave_pantry_lot ||--o{ recipeweave_pantry_consumption : "lot_id"
    recipeweave_unit ||--o{ recipeweave_pantry_consumption : "unit_id"
    recipeweave_pantry_lot {
        uuid id PK
        timestamptz created_at
        uuid user_id
        uuid form_id
        uuid product_version_id
        numeric_20_6_ amount
        uuid unit_id
        date expires_on
        timestamptz opened_at
        text location
        text priority
        text status
        uuid source_import_id
        text quantity_quality
        uuid original_form_id
        numeric_20_6_ original_amount
        uuid original_unit_id
        timestamptz updated_at
        boolean edited
    }
    recipeweave_app_user ||--o{ recipeweave_pantry_lot : "user_id"
    recipeweave_food_form ||--o{ recipeweave_pantry_lot : "form_id"
    recipeweave_product_version |o--o{ recipeweave_pantry_lot : "product_version_id"
    recipeweave_unit ||--o{ recipeweave_pantry_lot : "unit_id"
    recipeweave_receipt_import |o--o{ recipeweave_pantry_lot : "source_import_id"
    recipeweave_food_form |o--o{ recipeweave_pantry_lot : "original_form_id"
    recipeweave_unit |o--o{ recipeweave_pantry_lot : "original_unit_id"
    recipeweave_product {
        uuid id PK
        timestamptz created_at
        uuid food_id
        text brand
        text name
        text gtin
        text status
    }
    recipeweave_food ||--o{ recipeweave_product : "food_id"
    recipeweave_product_allergen {
        uuid id PK
        timestamptz created_at
        uuid product_version_id
        uuid allergen_id
        text presence
        uuid source_id
    }
    recipeweave_product_version ||--o{ recipeweave_product_allergen : "product_version_id"
    recipeweave_allergen ||--o{ recipeweave_product_allergen : "allergen_id"
    recipeweave_source_record ||--o{ recipeweave_product_allergen : "source_id"
    recipeweave_product_component {
        uuid id PK
        timestamptz created_at
        uuid product_version_id
        uuid form_id
        text name
        numeric_20_6_ amount
        uuid unit_id
        text quality
    }
    recipeweave_product_version ||--o{ recipeweave_product_component : "product_version_id"
    recipeweave_food_form ||--o{ recipeweave_product_component : "form_id"
    recipeweave_unit |o--o{ recipeweave_product_component : "unit_id"
    recipeweave_product_preparation_rule {
        uuid id PK
        timestamptz created_at
        uuid product_version_id
        uuid operation_id
        boolean allowed
        boolean use_original_container
        jsonb parameter_contract
        uuid source_id
    }
    recipeweave_product_version ||--o{ recipeweave_product_preparation_rule : "product_version_id"
    recipeweave_operation ||--o{ recipeweave_product_preparation_rule : "operation_id"
    recipeweave_source_record ||--o{ recipeweave_product_preparation_rule : "source_id"
    recipeweave_product_version {
        uuid id PK
        timestamptz created_at
        uuid product_id
        integer version
        uuid form_id
        numeric_20_6_ net_amount
        uuid unit_id
        numeric_20_6_ drain_amount
        uuid source_id
        text preparation_note
        date valid_from
    }
    recipeweave_product ||--o{ recipeweave_product_version : "product_id"
    recipeweave_food_form ||--o{ recipeweave_product_version : "form_id"
    recipeweave_unit ||--o{ recipeweave_product_version : "unit_id"
    recipeweave_source_record ||--o{ recipeweave_product_version : "source_id"
    recipeweave_receipt_import {
        uuid id PK
        timestamptz created_at
        uuid user_id
        char_64_ file_sha256
        text idempotency_key
        text status
        bigint revision
        timestamptz committed_at
        timestamptz reverted_at
        integer undo_preserved_count
    }
    recipeweave_app_user ||--o{ recipeweave_receipt_import : "user_id"
    recipeweave_receipt_line {
        uuid id PK
        timestamptz created_at
        uuid import_id
        integer line_no
        text raw_name
        uuid form_id
        uuid product_version_id
        numeric_20_6_ amount
        uuid unit_id
        text decision
        uuid pantry_lot_id
    }
    recipeweave_receipt_import ||--o{ recipeweave_receipt_line : "import_id"
    recipeweave_food_form |o--o{ recipeweave_receipt_line : "form_id"
    recipeweave_product_version |o--o{ recipeweave_receipt_line : "product_version_id"
    recipeweave_unit |o--o{ recipeweave_receipt_line : "unit_id"
    recipeweave_pantry_lot |o--o{ recipeweave_receipt_line : "pantry_lot_id"
    recipeweave_recipe {
        uuid id PK
        timestamptz created_at
        text title
        uuid family_option_id
        text status
        text withdrawal_reason
    }
    recipeweave_axis_option ||--o{ recipeweave_recipe : "family_option_id"
    recipeweave_recipe_embedding {
        uuid id PK
        timestamptz created_at
        uuid recipe_version_id
        text model_version
        char_64_ content_hash
        vector_768_ embedding
        text created_for_index
    }
    recipeweave_recipe_version ||--o{ recipeweave_recipe_embedding : "recipe_version_id"
    recipeweave_recipe_ingredient {
        uuid id PK
        timestamptz created_at
        uuid recipe_version_id
        integer line_no
        uuid form_id
        uuid product_version_id
        uuid component_id
        uuid kit_parent_line_id
        text role
        text demand_kind
        text amount_mode
        numeric_20_6_ amount
        numeric_20_6_ amount_max
        uuid unit_id
        numeric_20_6_ canonical_amount
        uuid conversion_id
        uuid scaling_rule_id
        boolean optional
        text note
    }
    recipeweave_recipe_version ||--o{ recipeweave_recipe_ingredient : "recipe_version_id"
    recipeweave_food_form ||--o{ recipeweave_recipe_ingredient : "form_id"
    recipeweave_product_version |o--o{ recipeweave_recipe_ingredient : "product_version_id"
    recipeweave_product_component |o--o{ recipeweave_recipe_ingredient : "component_id"
    recipeweave_recipe_ingredient |o--o{ recipeweave_recipe_ingredient : "kit_parent_line_id"
    recipeweave_unit ||--o{ recipeweave_recipe_ingredient : "unit_id"
    recipeweave_conversion |o--o{ recipeweave_recipe_ingredient : "conversion_id"
    recipeweave_scaling_rule ||--o{ recipeweave_recipe_ingredient : "scaling_rule_id"
    recipeweave_recipe_option {
        uuid id PK
        timestamptz created_at
        uuid recipe_version_id
        uuid option_id
    }
    recipeweave_recipe_version ||--o{ recipeweave_recipe_option : "recipe_version_id"
    recipeweave_axis_option ||--o{ recipeweave_recipe_option : "option_id"
    recipeweave_recipe_search_document {
        uuid id PK
        timestamptz created_at
        uuid recipe_id
        uuid published_version_id
        text projection_version
        text display_title
        uuid__ food_identity_ids
        uuid__ facet_option_ids
        text search_text
        boolean eligible
        char_64_ source_hash
        timestamptz projected_at
    }
    recipeweave_recipe ||--o| recipeweave_recipe_search_document : "recipe_id"
    recipeweave_recipe_version ||--o{ recipeweave_recipe_search_document : "published_version_id"
    recipeweave_recipe_signature {
        uuid id PK
        timestamptz created_at
        uuid recipe_version_id
        text algorithm_version
        char_64_ exact_hash
        jsonb canonical_payload
        text cluster_key
    }
    recipeweave_recipe_version ||--o{ recipeweave_recipe_signature : "recipe_version_id"
    recipeweave_recipe_similarity {
        uuid id PK
        timestamptz created_at
        uuid left_version_id
        uuid right_version_id
        text algorithm_version
        numeric_20_6_ score
        text explanation
    }
    recipeweave_recipe_version ||--o{ recipeweave_recipe_similarity : "left_version_id"
    recipeweave_recipe_version ||--o{ recipeweave_recipe_similarity : "right_version_id"
    recipeweave_recipe_step {
        uuid id PK
        timestamptz created_at
        uuid recipe_version_id
        integer step_no
        uuid operation_id
        text instruction
        text attention
        integer duration_min_s
        integer duration_max_s
        uuid scaling_rule_id
        text completion_cue
        text title
    }
    recipeweave_recipe_version ||--o{ recipeweave_recipe_step : "recipe_version_id"
    recipeweave_operation ||--o{ recipeweave_recipe_step : "operation_id"
    recipeweave_scaling_rule ||--o{ recipeweave_recipe_step : "scaling_rule_id"
    recipeweave_recipe_version {
        uuid id PK
        timestamptz created_at
        uuid recipe_id
        integer version
        uuid release_id
        numeric_20_6_ base_servings
        numeric_20_6_ output_amount
        uuid output_unit_id
        text status
        text validation
        char_64_ content_hash
        timestamptz published_at
        text description
    }
    recipeweave_recipe ||--o{ recipeweave_recipe_version : "recipe_id"
    recipeweave_catalog_release ||--o{ recipeweave_recipe_version : "release_id"
    recipeweave_unit ||--o{ recipeweave_recipe_version : "output_unit_id"
    recipeweave_resource_reservation {
        uuid id PK
        timestamptz created_at
        uuid task_id
        uuid resource_id
        integer start_s
        integer end_s
        integer quantity
    }
    recipeweave_session_task ||--o{ recipeweave_resource_reservation : "task_id"
    recipeweave_kitchen_resource ||--o{ recipeweave_resource_reservation : "resource_id"
    recipeweave_resource_type {
        uuid id PK
        timestamptz created_at
        text code
        text name
        uuid capacity_unit_id
        text status
    }
    recipeweave_unit |o--o{ recipeweave_resource_type : "capacity_unit_id"
    recipeweave_scaling_point {
        uuid id PK
        timestamptz created_at
        uuid rule_id
        numeric_20_6_ servings
        numeric_20_6_ multiplier
    }
    recipeweave_scaling_rule ||--o{ recipeweave_scaling_point : "rule_id"
    recipeweave_scaling_rule {
        uuid id PK
        timestamptz created_at
        text name
        text mode
        numeric_20_6_ min_servings
        numeric_20_6_ max_servings
        numeric_20_6_ batch_capacity
        text round_mode
        numeric_20_6_ round_increment
        uuid source_id
    }
    recipeweave_source_record |o--o{ recipeweave_scaling_rule : "source_id"
    recipeweave_schema_migrations {
        TEXT id PK
        TEXT checksum
        TIMESTAMPTZ applied_at
    }
    recipeweave_session_task {
        uuid id PK
        timestamptz created_at
        uuid session_id
        uuid menu_item_id
        uuid step_id
        integer batch_no
        integer planned_start_s
        integer planned_end_s
        text status
        timestamptz actual_start_at
        timestamptz actual_end_at
        timestamptz timer_started_at
        integer timer_duration_s
    }
    recipeweave_cooking_session ||--o{ recipeweave_session_task : "session_id"
    recipeweave_menu_item ||--o{ recipeweave_session_task : "menu_item_id"
    recipeweave_recipe_step ||--o{ recipeweave_session_task : "step_id"
    recipeweave_shopping_item {
        uuid id PK
        timestamptz created_at
        uuid session_id
        uuid total_id
        uuid product_version_id
        numeric_20_6_ net_shortage
        integer package_count
        numeric_20_6_ surplus_amount
        boolean checked
        text client_key
        timestamptz checked_at
        boolean archived
    }
    recipeweave_cooking_session ||--o{ recipeweave_shopping_item : "session_id"
    recipeweave_ingredient_total ||--o{ recipeweave_shopping_item : "total_id"
    recipeweave_product_version |o--o{ recipeweave_shopping_item : "product_version_id"
    recipeweave_source_record {
        uuid id PK
        timestamptz created_at
        text title
        text url
        text locator
        timestamptz retrieved_at
        char_64_ content_hash
        text license_note
    }
    recipeweave_step_dependency {
        uuid id PK
        timestamptz created_at
        uuid before_step_id
        uuid after_step_id
        text kind
        integer min_lag_s
        integer max_lag_s
    }
    recipeweave_recipe_step ||--o{ recipeweave_step_dependency : "before_step_id"
    recipeweave_recipe_step ||--o{ recipeweave_step_dependency : "after_step_id"
    recipeweave_step_input {
        uuid id PK
        timestamptz created_at
        uuid step_id
        uuid material_id
        numeric_20_6_ fraction
    }
    recipeweave_recipe_step ||--o{ recipeweave_step_input : "step_id"
    recipeweave_material_node ||--o{ recipeweave_step_input : "material_id"
    recipeweave_step_media {
        uuid id PK
        timestamptz created_at
        uuid step_id
        uuid media_id
        integer start_ms
        integer end_ms
    }
    recipeweave_recipe_step ||--o{ recipeweave_step_media : "step_id"
    recipeweave_media_asset ||--o{ recipeweave_step_media : "media_id"
    recipeweave_step_parameter {
        uuid id PK
        timestamptz created_at
        uuid step_id
        uuid parameter_id
        numeric_20_6_ number_value
        text text_value
        boolean bool_value
    }
    recipeweave_recipe_step ||--o{ recipeweave_step_parameter : "step_id"
    recipeweave_operation_parameter ||--o{ recipeweave_step_parameter : "parameter_id"
    recipeweave_step_resource {
        uuid id PK
        timestamptz created_at
        uuid step_id
        uuid resource_type_id
        integer quantity
        numeric_20_6_ capacity_min
        boolean exclusive
    }
    recipeweave_recipe_step ||--o{ recipeweave_step_resource : "step_id"
    recipeweave_resource_type ||--o{ recipeweave_step_resource : "resource_type_id"
    recipeweave_task_dependency {
        uuid id PK
        timestamptz created_at
        uuid before_task_id
        uuid after_task_id
        integer min_lag_s
        integer max_lag_s
        text reason
    }
    recipeweave_session_task ||--o{ recipeweave_task_dependency : "before_task_id"
    recipeweave_session_task ||--o{ recipeweave_task_dependency : "after_task_id"
    recipeweave_unit {
        uuid id PK
        timestamptz created_at
        text code
        text name
        text dimension
        numeric_20_6_ factor
        numeric_20_6_ offset
        text status
    }
    recipeweave_user_exclusion {
        uuid id PK
        timestamptz created_at
        uuid user_id
        uuid food_id
        uuid allergen_id
        boolean strict
    }
    recipeweave_app_user ||--o{ recipeweave_user_exclusion : "user_id"
    recipeweave_food |o--o{ recipeweave_user_exclusion : "food_id"
    recipeweave_allergen |o--o{ recipeweave_user_exclusion : "allergen_id"
    recipeweave_user_food {
        uuid id PK
        timestamptz created_at
        uuid user_id
        uuid food_id
    }
    recipeweave_app_user ||--o{ recipeweave_user_food : "user_id"
    recipeweave_food ||--o| recipeweave_user_food : "food_id"
    recipeweave_user_pantry_food {
        uuid id PK
        timestamptz created_at
        uuid user_id
        uuid food_id
    }
    recipeweave_app_user ||--o{ recipeweave_user_pantry_food : "user_id"
    recipeweave_food ||--o{ recipeweave_user_pantry_food : "food_id"
    recipeweave_user_preference {
        uuid id PK
        timestamptz created_at
        uuid user_id
        uuid option_id
        numeric_20_6_ weight
    }
    recipeweave_app_user ||--o{ recipeweave_user_preference : "user_id"
    recipeweave_axis_option ||--o{ recipeweave_user_preference : "option_id"
    recipeweave_user_recipe_event {
        uuid id PK
        timestamptz created_at
        uuid user_id
        uuid recipe_version_id
        text kind
        timestamptz occurred_at
        text request_key
    }
    recipeweave_app_user ||--o{ recipeweave_user_recipe_event : "user_id"
    recipeweave_recipe_version ||--o{ recipeweave_user_recipe_event : "recipe_version_id"
    recipeweave_user_shopping_check {
        uuid id PK
        timestamptz created_at
        uuid user_id
        text key
        text signature
        uuid food_id
        numeric_20_6_ amount
        uuid unit_id
        timestamptz checked_at
        boolean archived
    }
    recipeweave_app_user ||--o{ recipeweave_user_shopping_check : "user_id"
    recipeweave_food |o--o{ recipeweave_user_shopping_check : "food_id"
    recipeweave_unit |o--o{ recipeweave_user_shopping_check : "unit_id"
    recipeweave_user_state {
        text subject PK
        bigint revision
        jsonb payload
        timestamptz updated_at
    }
    recipeweave_validation_result {
        uuid id PK
        timestamptz created_at
        uuid recipe_version_id
        uuid rule_id
        text state
        jsonb evidence
        text validator_version
        timestamptz evaluated_at
    }
    recipeweave_recipe_version ||--o{ recipeweave_validation_result : "recipe_version_id"
    recipeweave_compatibility_rule ||--o{ recipeweave_validation_result : "rule_id"
    recipeweave_workspace_revision {
        uuid id PK
        timestamptz created_at
        uuid user_id
        bigint revision
    }
    recipeweave_app_user ||--o| recipeweave_workspace_revision : "user_id"
```

線はDDLの外部キー定義に基づく。実データの件数やアプリ上の関連を追加推測しない。
