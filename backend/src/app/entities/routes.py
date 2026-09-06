# generate_entity_apis.py による自動生成。直接編集しない。
from fastapi import FastAPI

from app.apis.entities.allergen_create.router import router as entity_allergen_create
from app.apis.entities.allergen_get.router import router as entity_allergen_get
from app.apis.entities.allergen_list.router import router as entity_allergen_list
from app.apis.entities.allergen_update.router import router as entity_allergen_update
from app.apis.entities.app_user_get.router import router as entity_app_user_get
from app.apis.entities.app_user_list.router import router as entity_app_user_list
from app.apis.entities.app_user_update.router import router as entity_app_user_update
from app.apis.entities.audit_event_get.router import router as entity_audit_event_get
from app.apis.entities.audit_event_list.router import router as entity_audit_event_list
from app.apis.entities.axis_create.router import router as entity_axis_create
from app.apis.entities.axis_get.router import router as entity_axis_get
from app.apis.entities.axis_list.router import router as entity_axis_list
from app.apis.entities.axis_option_create.router import router as entity_axis_option_create
from app.apis.entities.axis_option_get.router import router as entity_axis_option_get
from app.apis.entities.axis_option_list.router import router as entity_axis_option_list
from app.apis.entities.axis_option_update.router import router as entity_axis_option_update
from app.apis.entities.axis_update.router import router as entity_axis_update
from app.apis.entities.backup_artifact_get.router import router as entity_backup_artifact_get
from app.apis.entities.backup_artifact_list.router import router as entity_backup_artifact_list
from app.apis.entities.backup_restore_intent_get.router import (
    router as entity_backup_restore_intent_get,
)
from app.apis.entities.backup_restore_intent_list.router import (
    router as entity_backup_restore_intent_list,
)
from app.apis.entities.candidate_attempt_create.router import (
    router as entity_candidate_attempt_create,
)
from app.apis.entities.candidate_attempt_get.router import router as entity_candidate_attempt_get
from app.apis.entities.candidate_attempt_list.router import router as entity_candidate_attempt_list
from app.apis.entities.candidate_attempt_update.router import (
    router as entity_candidate_attempt_update,
)
from app.apis.entities.catalog_release_create.router import router as entity_catalog_release_create
from app.apis.entities.catalog_release_get.router import router as entity_catalog_release_get
from app.apis.entities.catalog_release_list.router import router as entity_catalog_release_list
from app.apis.entities.catalog_release_update.router import router as entity_catalog_release_update
from app.apis.entities.compatibility_rule_create.router import (
    router as entity_compatibility_rule_create,
)
from app.apis.entities.compatibility_rule_get.router import router as entity_compatibility_rule_get
from app.apis.entities.compatibility_rule_list.router import (
    router as entity_compatibility_rule_list,
)
from app.apis.entities.conversion_create.router import router as entity_conversion_create
from app.apis.entities.conversion_get.router import router as entity_conversion_get
from app.apis.entities.conversion_list.router import router as entity_conversion_list
from app.apis.entities.conversion_update.router import router as entity_conversion_update
from app.apis.entities.cooking_session_create.router import router as entity_cooking_session_create
from app.apis.entities.cooking_session_delete.router import router as entity_cooking_session_delete
from app.apis.entities.cooking_session_get.router import router as entity_cooking_session_get
from app.apis.entities.cooking_session_list.router import router as entity_cooking_session_list
from app.apis.entities.cooking_session_update.router import router as entity_cooking_session_update
from app.apis.entities.food_alias_create.router import router as entity_food_alias_create
from app.apis.entities.food_alias_get.router import router as entity_food_alias_get
from app.apis.entities.food_alias_list.router import router as entity_food_alias_list
from app.apis.entities.food_alias_update.router import router as entity_food_alias_update
from app.apis.entities.food_allergen_create.router import router as entity_food_allergen_create
from app.apis.entities.food_allergen_get.router import router as entity_food_allergen_get
from app.apis.entities.food_allergen_list.router import router as entity_food_allergen_list
from app.apis.entities.food_axis_option_create.router import (
    router as entity_food_axis_option_create,
)
from app.apis.entities.food_axis_option_get.router import router as entity_food_axis_option_get
from app.apis.entities.food_axis_option_list.router import router as entity_food_axis_option_list
from app.apis.entities.food_axis_option_update.router import (
    router as entity_food_axis_option_update,
)
from app.apis.entities.food_create.router import router as entity_food_create
from app.apis.entities.food_form_create.router import router as entity_food_form_create
from app.apis.entities.food_form_get.router import router as entity_food_form_get
from app.apis.entities.food_form_list.router import router as entity_food_form_list
from app.apis.entities.food_form_update.router import router as entity_food_form_update
from app.apis.entities.food_get.router import router as entity_food_get
from app.apis.entities.food_identity_create.router import router as entity_food_identity_create
from app.apis.entities.food_identity_get.router import router as entity_food_identity_get
from app.apis.entities.food_identity_list.router import router as entity_food_identity_list
from app.apis.entities.food_identity_member_create.router import (
    router as entity_food_identity_member_create,
)
from app.apis.entities.food_identity_member_get.router import (
    router as entity_food_identity_member_get,
)
from app.apis.entities.food_identity_member_list.router import (
    router as entity_food_identity_member_list,
)
from app.apis.entities.food_list.router import router as entity_food_list
from app.apis.entities.food_update.router import router as entity_food_update
from app.apis.entities.form_yield_create.router import router as entity_form_yield_create
from app.apis.entities.form_yield_get.router import router as entity_form_yield_get
from app.apis.entities.form_yield_list.router import router as entity_form_yield_list
from app.apis.entities.generation_choice_create.router import (
    router as entity_generation_choice_create,
)
from app.apis.entities.generation_choice_get.router import router as entity_generation_choice_get
from app.apis.entities.generation_choice_list.router import router as entity_generation_choice_list
from app.apis.entities.generation_choice_update.router import (
    router as entity_generation_choice_update,
)
from app.apis.entities.generation_food_create.router import router as entity_generation_food_create
from app.apis.entities.generation_food_get.router import router as entity_generation_food_get
from app.apis.entities.generation_food_list.router import router as entity_generation_food_list
from app.apis.entities.generation_food_update.router import router as entity_generation_food_update
from app.apis.entities.generation_job_create.router import router as entity_generation_job_create
from app.apis.entities.generation_job_get.router import router as entity_generation_job_get
from app.apis.entities.generation_job_list.router import router as entity_generation_job_list
from app.apis.entities.generation_job_update.router import router as entity_generation_job_update
from app.apis.entities.generation_policy_create.router import (
    router as entity_generation_policy_create,
)
from app.apis.entities.generation_policy_get.router import router as entity_generation_policy_get
from app.apis.entities.generation_policy_list.router import router as entity_generation_policy_list
from app.apis.entities.generation_result_create.router import (
    router as entity_generation_result_create,
)
from app.apis.entities.generation_result_get.router import router as entity_generation_result_get
from app.apis.entities.generation_result_list.router import router as entity_generation_result_list
from app.apis.entities.generation_shard_create.router import (
    router as entity_generation_shard_create,
)
from app.apis.entities.generation_shard_get.router import router as entity_generation_shard_get
from app.apis.entities.generation_shard_list.router import router as entity_generation_shard_list
from app.apis.entities.generation_stratum_metric_create.router import (
    router as entity_generation_stratum_metric_create,
)
from app.apis.entities.generation_stratum_metric_get.router import (
    router as entity_generation_stratum_metric_get,
)
from app.apis.entities.generation_stratum_metric_list.router import (
    router as entity_generation_stratum_metric_list,
)
from app.apis.entities.generation_template_create.router import (
    router as entity_generation_template_create,
)
from app.apis.entities.generation_template_get.router import (
    router as entity_generation_template_get,
)
from app.apis.entities.generation_template_list.router import (
    router as entity_generation_template_list,
)
from app.apis.entities.ingredient_total_get.router import router as entity_ingredient_total_get
from app.apis.entities.ingredient_total_list.router import router as entity_ingredient_total_list
from app.apis.entities.kitchen_resource_create.router import (
    router as entity_kitchen_resource_create,
)
from app.apis.entities.kitchen_resource_delete.router import (
    router as entity_kitchen_resource_delete,
)
from app.apis.entities.kitchen_resource_get.router import router as entity_kitchen_resource_get
from app.apis.entities.kitchen_resource_list.router import router as entity_kitchen_resource_list
from app.apis.entities.kitchen_resource_update.router import (
    router as entity_kitchen_resource_update,
)
from app.apis.entities.material_node_create.router import router as entity_material_node_create
from app.apis.entities.material_node_get.router import router as entity_material_node_get
from app.apis.entities.material_node_list.router import router as entity_material_node_list
from app.apis.entities.material_node_update.router import router as entity_material_node_update
from app.apis.entities.media_asset_create.router import router as entity_media_asset_create
from app.apis.entities.media_asset_get.router import router as entity_media_asset_get
from app.apis.entities.media_asset_list.router import router as entity_media_asset_list
from app.apis.entities.menu_create.router import router as entity_menu_create
from app.apis.entities.menu_delete.router import router as entity_menu_delete
from app.apis.entities.menu_get.router import router as entity_menu_get
from app.apis.entities.menu_ingredient_override_create.router import (
    router as entity_menu_ingredient_override_create,
)
from app.apis.entities.menu_ingredient_override_delete.router import (
    router as entity_menu_ingredient_override_delete,
)
from app.apis.entities.menu_ingredient_override_get.router import (
    router as entity_menu_ingredient_override_get,
)
from app.apis.entities.menu_ingredient_override_list.router import (
    router as entity_menu_ingredient_override_list,
)
from app.apis.entities.menu_ingredient_override_update.router import (
    router as entity_menu_ingredient_override_update,
)
from app.apis.entities.menu_item_create.router import router as entity_menu_item_create
from app.apis.entities.menu_item_delete.router import router as entity_menu_item_delete
from app.apis.entities.menu_item_get.router import router as entity_menu_item_get
from app.apis.entities.menu_item_list.router import router as entity_menu_item_list
from app.apis.entities.menu_item_update.router import router as entity_menu_item_update
from app.apis.entities.menu_list.router import router as entity_menu_list
from app.apis.entities.menu_update.router import router as entity_menu_update
from app.apis.entities.nutrient_create.router import router as entity_nutrient_create
from app.apis.entities.nutrient_get.router import router as entity_nutrient_get
from app.apis.entities.nutrient_list.router import router as entity_nutrient_list
from app.apis.entities.nutrient_update.router import router as entity_nutrient_update
from app.apis.entities.nutrition_fact_create.router import router as entity_nutrition_fact_create
from app.apis.entities.nutrition_fact_get.router import router as entity_nutrition_fact_get
from app.apis.entities.nutrition_fact_list.router import router as entity_nutrition_fact_list
from app.apis.entities.operation_create.router import router as entity_operation_create
from app.apis.entities.operation_get.router import router as entity_operation_get
from app.apis.entities.operation_list.router import router as entity_operation_list
from app.apis.entities.operation_parameter_create.router import (
    router as entity_operation_parameter_create,
)
from app.apis.entities.operation_parameter_get.router import (
    router as entity_operation_parameter_get,
)
from app.apis.entities.operation_parameter_list.router import (
    router as entity_operation_parameter_list,
)
from app.apis.entities.operation_parameter_update.router import (
    router as entity_operation_parameter_update,
)
from app.apis.entities.operation_update.router import router as entity_operation_update
from app.apis.entities.outbox_event_get.router import router as entity_outbox_event_get
from app.apis.entities.outbox_event_list.router import router as entity_outbox_event_list
from app.apis.entities.pantry_consumption_get.router import router as entity_pantry_consumption_get
from app.apis.entities.pantry_consumption_list.router import (
    router as entity_pantry_consumption_list,
)
from app.apis.entities.pantry_lot_create.router import router as entity_pantry_lot_create
from app.apis.entities.pantry_lot_delete.router import router as entity_pantry_lot_delete
from app.apis.entities.pantry_lot_get.router import router as entity_pantry_lot_get
from app.apis.entities.pantry_lot_list.router import router as entity_pantry_lot_list
from app.apis.entities.pantry_lot_update.router import router as entity_pantry_lot_update
from app.apis.entities.product_allergen_create.router import (
    router as entity_product_allergen_create,
)
from app.apis.entities.product_allergen_get.router import router as entity_product_allergen_get
from app.apis.entities.product_allergen_list.router import router as entity_product_allergen_list
from app.apis.entities.product_component_create.router import (
    router as entity_product_component_create,
)
from app.apis.entities.product_component_get.router import router as entity_product_component_get
from app.apis.entities.product_component_list.router import router as entity_product_component_list
from app.apis.entities.product_create.router import router as entity_product_create
from app.apis.entities.product_get.router import router as entity_product_get
from app.apis.entities.product_list.router import router as entity_product_list
from app.apis.entities.product_preparation_rule_create.router import (
    router as entity_product_preparation_rule_create,
)
from app.apis.entities.product_preparation_rule_get.router import (
    router as entity_product_preparation_rule_get,
)
from app.apis.entities.product_preparation_rule_list.router import (
    router as entity_product_preparation_rule_list,
)
from app.apis.entities.product_update.router import router as entity_product_update
from app.apis.entities.product_version_create.router import router as entity_product_version_create
from app.apis.entities.product_version_get.router import router as entity_product_version_get
from app.apis.entities.product_version_list.router import router as entity_product_version_list
from app.apis.entities.receipt_import_create.router import router as entity_receipt_import_create
from app.apis.entities.receipt_import_delete.router import router as entity_receipt_import_delete
from app.apis.entities.receipt_import_get.router import router as entity_receipt_import_get
from app.apis.entities.receipt_import_list.router import router as entity_receipt_import_list
from app.apis.entities.receipt_import_update.router import router as entity_receipt_import_update
from app.apis.entities.receipt_line_create.router import router as entity_receipt_line_create
from app.apis.entities.receipt_line_delete.router import router as entity_receipt_line_delete
from app.apis.entities.receipt_line_get.router import router as entity_receipt_line_get
from app.apis.entities.receipt_line_list.router import router as entity_receipt_line_list
from app.apis.entities.receipt_line_update.router import router as entity_receipt_line_update
from app.apis.entities.recipe_create.router import router as entity_recipe_create
from app.apis.entities.recipe_embedding_create.router import (
    router as entity_recipe_embedding_create,
)
from app.apis.entities.recipe_embedding_get.router import router as entity_recipe_embedding_get
from app.apis.entities.recipe_embedding_list.router import router as entity_recipe_embedding_list
from app.apis.entities.recipe_embedding_update.router import (
    router as entity_recipe_embedding_update,
)
from app.apis.entities.recipe_get.router import router as entity_recipe_get
from app.apis.entities.recipe_ingredient_create.router import (
    router as entity_recipe_ingredient_create,
)
from app.apis.entities.recipe_ingredient_get.router import router as entity_recipe_ingredient_get
from app.apis.entities.recipe_ingredient_list.router import router as entity_recipe_ingredient_list
from app.apis.entities.recipe_ingredient_update.router import (
    router as entity_recipe_ingredient_update,
)
from app.apis.entities.recipe_list.router import router as entity_recipe_list
from app.apis.entities.recipe_option_create.router import router as entity_recipe_option_create
from app.apis.entities.recipe_option_get.router import router as entity_recipe_option_get
from app.apis.entities.recipe_option_list.router import router as entity_recipe_option_list
from app.apis.entities.recipe_option_update.router import router as entity_recipe_option_update
from app.apis.entities.recipe_search_document_get.router import (
    router as entity_recipe_search_document_get,
)
from app.apis.entities.recipe_search_document_list.router import (
    router as entity_recipe_search_document_list,
)
from app.apis.entities.recipe_signature_create.router import (
    router as entity_recipe_signature_create,
)
from app.apis.entities.recipe_signature_get.router import router as entity_recipe_signature_get
from app.apis.entities.recipe_signature_list.router import router as entity_recipe_signature_list
from app.apis.entities.recipe_similarity_create.router import (
    router as entity_recipe_similarity_create,
)
from app.apis.entities.recipe_similarity_get.router import router as entity_recipe_similarity_get
from app.apis.entities.recipe_similarity_list.router import router as entity_recipe_similarity_list
from app.apis.entities.recipe_similarity_update.router import (
    router as entity_recipe_similarity_update,
)
from app.apis.entities.recipe_step_create.router import router as entity_recipe_step_create
from app.apis.entities.recipe_step_get.router import router as entity_recipe_step_get
from app.apis.entities.recipe_step_list.router import router as entity_recipe_step_list
from app.apis.entities.recipe_step_update.router import router as entity_recipe_step_update
from app.apis.entities.recipe_update.router import router as entity_recipe_update
from app.apis.entities.recipe_version_create.router import router as entity_recipe_version_create
from app.apis.entities.recipe_version_get.router import router as entity_recipe_version_get
from app.apis.entities.recipe_version_list.router import router as entity_recipe_version_list
from app.apis.entities.recipe_version_update.router import router as entity_recipe_version_update
from app.apis.entities.resource_reservation_create.router import (
    router as entity_resource_reservation_create,
)
from app.apis.entities.resource_reservation_delete.router import (
    router as entity_resource_reservation_delete,
)
from app.apis.entities.resource_reservation_get.router import (
    router as entity_resource_reservation_get,
)
from app.apis.entities.resource_reservation_list.router import (
    router as entity_resource_reservation_list,
)
from app.apis.entities.resource_reservation_update.router import (
    router as entity_resource_reservation_update,
)
from app.apis.entities.resource_type_create.router import router as entity_resource_type_create
from app.apis.entities.resource_type_get.router import router as entity_resource_type_get
from app.apis.entities.resource_type_list.router import router as entity_resource_type_list
from app.apis.entities.resource_type_update.router import router as entity_resource_type_update
from app.apis.entities.scaling_point_create.router import router as entity_scaling_point_create
from app.apis.entities.scaling_point_get.router import router as entity_scaling_point_get
from app.apis.entities.scaling_point_list.router import router as entity_scaling_point_list
from app.apis.entities.scaling_rule_create.router import router as entity_scaling_rule_create
from app.apis.entities.scaling_rule_get.router import router as entity_scaling_rule_get
from app.apis.entities.scaling_rule_list.router import router as entity_scaling_rule_list
from app.apis.entities.session_task_create.router import router as entity_session_task_create
from app.apis.entities.session_task_delete.router import router as entity_session_task_delete
from app.apis.entities.session_task_get.router import router as entity_session_task_get
from app.apis.entities.session_task_list.router import router as entity_session_task_list
from app.apis.entities.session_task_update.router import router as entity_session_task_update
from app.apis.entities.shopping_item_create.router import router as entity_shopping_item_create
from app.apis.entities.shopping_item_delete.router import router as entity_shopping_item_delete
from app.apis.entities.shopping_item_get.router import router as entity_shopping_item_get
from app.apis.entities.shopping_item_list.router import router as entity_shopping_item_list
from app.apis.entities.shopping_item_update.router import router as entity_shopping_item_update
from app.apis.entities.source_record_create.router import router as entity_source_record_create
from app.apis.entities.source_record_get.router import router as entity_source_record_get
from app.apis.entities.source_record_list.router import router as entity_source_record_list
from app.apis.entities.source_record_update.router import router as entity_source_record_update
from app.apis.entities.step_dependency_create.router import router as entity_step_dependency_create
from app.apis.entities.step_dependency_get.router import router as entity_step_dependency_get
from app.apis.entities.step_dependency_list.router import router as entity_step_dependency_list
from app.apis.entities.step_dependency_update.router import router as entity_step_dependency_update
from app.apis.entities.step_input_create.router import router as entity_step_input_create
from app.apis.entities.step_input_get.router import router as entity_step_input_get
from app.apis.entities.step_input_list.router import router as entity_step_input_list
from app.apis.entities.step_input_update.router import router as entity_step_input_update
from app.apis.entities.step_media_create.router import router as entity_step_media_create
from app.apis.entities.step_media_get.router import router as entity_step_media_get
from app.apis.entities.step_media_list.router import router as entity_step_media_list
from app.apis.entities.step_media_update.router import router as entity_step_media_update
from app.apis.entities.step_parameter_create.router import router as entity_step_parameter_create
from app.apis.entities.step_parameter_get.router import router as entity_step_parameter_get
from app.apis.entities.step_parameter_list.router import router as entity_step_parameter_list
from app.apis.entities.step_parameter_update.router import router as entity_step_parameter_update
from app.apis.entities.step_resource_create.router import router as entity_step_resource_create
from app.apis.entities.step_resource_get.router import router as entity_step_resource_get
from app.apis.entities.step_resource_list.router import router as entity_step_resource_list
from app.apis.entities.step_resource_update.router import router as entity_step_resource_update
from app.apis.entities.task_dependency_create.router import router as entity_task_dependency_create
from app.apis.entities.task_dependency_delete.router import router as entity_task_dependency_delete
from app.apis.entities.task_dependency_get.router import router as entity_task_dependency_get
from app.apis.entities.task_dependency_list.router import router as entity_task_dependency_list
from app.apis.entities.task_dependency_update.router import router as entity_task_dependency_update
from app.apis.entities.unit_create.router import router as entity_unit_create
from app.apis.entities.unit_get.router import router as entity_unit_get
from app.apis.entities.unit_list.router import router as entity_unit_list
from app.apis.entities.unit_update.router import router as entity_unit_update
from app.apis.entities.user_exclusion_create.router import router as entity_user_exclusion_create
from app.apis.entities.user_exclusion_delete.router import router as entity_user_exclusion_delete
from app.apis.entities.user_exclusion_get.router import router as entity_user_exclusion_get
from app.apis.entities.user_exclusion_list.router import router as entity_user_exclusion_list
from app.apis.entities.user_exclusion_update.router import router as entity_user_exclusion_update
from app.apis.entities.user_food_create.router import router as entity_user_food_create
from app.apis.entities.user_food_delete.router import router as entity_user_food_delete
from app.apis.entities.user_food_get.router import router as entity_user_food_get
from app.apis.entities.user_food_list.router import router as entity_user_food_list
from app.apis.entities.user_food_update.router import router as entity_user_food_update
from app.apis.entities.user_pantry_food_create.router import (
    router as entity_user_pantry_food_create,
)
from app.apis.entities.user_pantry_food_delete.router import (
    router as entity_user_pantry_food_delete,
)
from app.apis.entities.user_pantry_food_get.router import router as entity_user_pantry_food_get
from app.apis.entities.user_pantry_food_list.router import router as entity_user_pantry_food_list
from app.apis.entities.user_pantry_food_update.router import (
    router as entity_user_pantry_food_update,
)
from app.apis.entities.user_preference_create.router import router as entity_user_preference_create
from app.apis.entities.user_preference_delete.router import router as entity_user_preference_delete
from app.apis.entities.user_preference_get.router import router as entity_user_preference_get
from app.apis.entities.user_preference_list.router import router as entity_user_preference_list
from app.apis.entities.user_preference_update.router import router as entity_user_preference_update
from app.apis.entities.user_recipe_event_create.router import (
    router as entity_user_recipe_event_create,
)
from app.apis.entities.user_recipe_event_delete.router import (
    router as entity_user_recipe_event_delete,
)
from app.apis.entities.user_recipe_event_get.router import router as entity_user_recipe_event_get
from app.apis.entities.user_recipe_event_list.router import router as entity_user_recipe_event_list
from app.apis.entities.user_shopping_check_create.router import (
    router as entity_user_shopping_check_create,
)
from app.apis.entities.user_shopping_check_delete.router import (
    router as entity_user_shopping_check_delete,
)
from app.apis.entities.user_shopping_check_get.router import (
    router as entity_user_shopping_check_get,
)
from app.apis.entities.user_shopping_check_list.router import (
    router as entity_user_shopping_check_list,
)
from app.apis.entities.user_shopping_check_update.router import (
    router as entity_user_shopping_check_update,
)
from app.apis.entities.validation_result_create.router import (
    router as entity_validation_result_create,
)
from app.apis.entities.validation_result_get.router import router as entity_validation_result_get
from app.apis.entities.validation_result_list.router import router as entity_validation_result_list
from app.apis.entities.workspace_revision_get.router import router as entity_workspace_revision_get
from app.apis.entities.workspace_revision_list.router import (
    router as entity_workspace_revision_list,
)
from app.entities.generation_routes import register_generation_routes


def register_entity_routes(application: FastAPI) -> None:
    """全テーブルの許可された固定ルートを登録する。"""
    application.include_router(entity_source_record_list)
    application.include_router(entity_source_record_get)
    application.include_router(entity_source_record_create)
    application.include_router(entity_source_record_update)
    application.include_router(entity_catalog_release_list)
    application.include_router(entity_catalog_release_get)
    application.include_router(entity_catalog_release_create)
    application.include_router(entity_catalog_release_update)
    application.include_router(entity_unit_list)
    application.include_router(entity_unit_get)
    application.include_router(entity_unit_create)
    application.include_router(entity_unit_update)
    application.include_router(entity_food_list)
    application.include_router(entity_food_get)
    application.include_router(entity_food_create)
    application.include_router(entity_food_update)
    application.include_router(entity_food_alias_list)
    application.include_router(entity_food_alias_get)
    application.include_router(entity_food_alias_create)
    application.include_router(entity_food_alias_update)
    application.include_router(entity_food_form_list)
    application.include_router(entity_food_form_get)
    application.include_router(entity_food_form_create)
    application.include_router(entity_food_form_update)
    application.include_router(entity_conversion_list)
    application.include_router(entity_conversion_get)
    application.include_router(entity_conversion_create)
    application.include_router(entity_conversion_update)
    application.include_router(entity_form_yield_list)
    application.include_router(entity_form_yield_get)
    application.include_router(entity_form_yield_create)
    application.include_router(entity_product_list)
    application.include_router(entity_product_get)
    application.include_router(entity_product_create)
    application.include_router(entity_product_update)
    application.include_router(entity_product_version_list)
    application.include_router(entity_product_version_get)
    application.include_router(entity_product_version_create)
    application.include_router(entity_product_component_list)
    application.include_router(entity_product_component_get)
    application.include_router(entity_product_component_create)
    application.include_router(entity_allergen_list)
    application.include_router(entity_allergen_get)
    application.include_router(entity_allergen_create)
    application.include_router(entity_allergen_update)
    application.include_router(entity_food_allergen_list)
    application.include_router(entity_food_allergen_get)
    application.include_router(entity_food_allergen_create)
    application.include_router(entity_product_allergen_list)
    application.include_router(entity_product_allergen_get)
    application.include_router(entity_product_allergen_create)
    application.include_router(entity_nutrient_list)
    application.include_router(entity_nutrient_get)
    application.include_router(entity_nutrient_create)
    application.include_router(entity_nutrient_update)
    application.include_router(entity_nutrition_fact_list)
    application.include_router(entity_nutrition_fact_get)
    application.include_router(entity_nutrition_fact_create)
    application.include_router(entity_axis_list)
    application.include_router(entity_axis_get)
    application.include_router(entity_axis_create)
    application.include_router(entity_axis_update)
    application.include_router(entity_axis_option_list)
    application.include_router(entity_axis_option_get)
    application.include_router(entity_axis_option_create)
    application.include_router(entity_axis_option_update)
    application.include_router(entity_food_axis_option_list)
    application.include_router(entity_food_axis_option_get)
    application.include_router(entity_food_axis_option_create)
    application.include_router(entity_food_axis_option_update)
    application.include_router(entity_recipe_list)
    application.include_router(entity_recipe_get)
    application.include_router(entity_recipe_create)
    application.include_router(entity_recipe_update)
    application.include_router(entity_recipe_version_list)
    application.include_router(entity_recipe_version_get)
    application.include_router(entity_recipe_version_create)
    application.include_router(entity_recipe_version_update)
    application.include_router(entity_recipe_option_list)
    application.include_router(entity_recipe_option_get)
    application.include_router(entity_recipe_option_create)
    application.include_router(entity_recipe_option_update)
    application.include_router(entity_scaling_rule_list)
    application.include_router(entity_scaling_rule_get)
    application.include_router(entity_scaling_rule_create)
    application.include_router(entity_scaling_point_list)
    application.include_router(entity_scaling_point_get)
    application.include_router(entity_scaling_point_create)
    application.include_router(entity_recipe_ingredient_list)
    application.include_router(entity_recipe_ingredient_get)
    application.include_router(entity_recipe_ingredient_create)
    application.include_router(entity_recipe_ingredient_update)
    application.include_router(entity_operation_list)
    application.include_router(entity_operation_get)
    application.include_router(entity_operation_create)
    application.include_router(entity_operation_update)
    application.include_router(entity_operation_parameter_list)
    application.include_router(entity_operation_parameter_get)
    application.include_router(entity_operation_parameter_create)
    application.include_router(entity_operation_parameter_update)
    application.include_router(entity_recipe_step_list)
    application.include_router(entity_recipe_step_get)
    application.include_router(entity_recipe_step_create)
    application.include_router(entity_recipe_step_update)
    application.include_router(entity_step_parameter_list)
    application.include_router(entity_step_parameter_get)
    application.include_router(entity_step_parameter_create)
    application.include_router(entity_step_parameter_update)
    application.include_router(entity_material_node_list)
    application.include_router(entity_material_node_get)
    application.include_router(entity_material_node_create)
    application.include_router(entity_material_node_update)
    application.include_router(entity_step_input_list)
    application.include_router(entity_step_input_get)
    application.include_router(entity_step_input_create)
    application.include_router(entity_step_input_update)
    application.include_router(entity_step_dependency_list)
    application.include_router(entity_step_dependency_get)
    application.include_router(entity_step_dependency_create)
    application.include_router(entity_step_dependency_update)
    application.include_router(entity_resource_type_list)
    application.include_router(entity_resource_type_get)
    application.include_router(entity_resource_type_create)
    application.include_router(entity_resource_type_update)
    application.include_router(entity_step_resource_list)
    application.include_router(entity_step_resource_get)
    application.include_router(entity_step_resource_create)
    application.include_router(entity_step_resource_update)
    application.include_router(entity_media_asset_list)
    application.include_router(entity_media_asset_get)
    application.include_router(entity_media_asset_create)
    application.include_router(entity_step_media_list)
    application.include_router(entity_step_media_get)
    application.include_router(entity_step_media_create)
    application.include_router(entity_step_media_update)
    application.include_router(entity_generation_policy_list)
    application.include_router(entity_generation_policy_get)
    application.include_router(entity_generation_policy_create)
    application.include_router(entity_generation_job_list)
    application.include_router(entity_generation_job_get)
    application.include_router(entity_generation_job_create)
    application.include_router(entity_generation_job_update)
    application.include_router(entity_generation_choice_list)
    application.include_router(entity_generation_choice_get)
    application.include_router(entity_generation_choice_create)
    application.include_router(entity_generation_choice_update)
    application.include_router(entity_generation_food_list)
    application.include_router(entity_generation_food_get)
    application.include_router(entity_generation_food_create)
    application.include_router(entity_generation_food_update)
    application.include_router(entity_generation_result_list)
    application.include_router(entity_generation_result_get)
    application.include_router(entity_generation_result_create)
    application.include_router(entity_compatibility_rule_list)
    application.include_router(entity_compatibility_rule_get)
    application.include_router(entity_compatibility_rule_create)
    application.include_router(entity_validation_result_list)
    application.include_router(entity_validation_result_get)
    application.include_router(entity_validation_result_create)
    application.include_router(entity_recipe_signature_list)
    application.include_router(entity_recipe_signature_get)
    application.include_router(entity_recipe_signature_create)
    application.include_router(entity_recipe_similarity_list)
    application.include_router(entity_recipe_similarity_get)
    application.include_router(entity_recipe_similarity_create)
    application.include_router(entity_recipe_similarity_update)
    application.include_router(entity_app_user_list)
    application.include_router(entity_app_user_get)
    application.include_router(entity_app_user_update)
    application.include_router(entity_user_preference_list)
    application.include_router(entity_user_preference_get)
    application.include_router(entity_user_preference_create)
    application.include_router(entity_user_preference_update)
    application.include_router(entity_user_preference_delete)
    application.include_router(entity_user_exclusion_list)
    application.include_router(entity_user_exclusion_get)
    application.include_router(entity_user_exclusion_create)
    application.include_router(entity_user_exclusion_update)
    application.include_router(entity_user_exclusion_delete)
    application.include_router(entity_user_recipe_event_list)
    application.include_router(entity_user_recipe_event_get)
    application.include_router(entity_user_recipe_event_create)
    application.include_router(entity_user_recipe_event_delete)
    application.include_router(entity_menu_list)
    application.include_router(entity_menu_get)
    application.include_router(entity_menu_create)
    application.include_router(entity_menu_update)
    application.include_router(entity_menu_delete)
    application.include_router(entity_menu_item_list)
    application.include_router(entity_menu_item_get)
    application.include_router(entity_menu_item_create)
    application.include_router(entity_menu_item_update)
    application.include_router(entity_menu_item_delete)
    application.include_router(entity_menu_ingredient_override_list)
    application.include_router(entity_menu_ingredient_override_get)
    application.include_router(entity_menu_ingredient_override_create)
    application.include_router(entity_menu_ingredient_override_update)
    application.include_router(entity_menu_ingredient_override_delete)
    application.include_router(entity_kitchen_resource_list)
    application.include_router(entity_kitchen_resource_get)
    application.include_router(entity_kitchen_resource_create)
    application.include_router(entity_kitchen_resource_update)
    application.include_router(entity_kitchen_resource_delete)
    application.include_router(entity_cooking_session_list)
    application.include_router(entity_cooking_session_get)
    application.include_router(entity_cooking_session_create)
    application.include_router(entity_cooking_session_update)
    application.include_router(entity_cooking_session_delete)
    application.include_router(entity_session_task_list)
    application.include_router(entity_session_task_get)
    application.include_router(entity_session_task_create)
    application.include_router(entity_session_task_update)
    application.include_router(entity_session_task_delete)
    application.include_router(entity_task_dependency_list)
    application.include_router(entity_task_dependency_get)
    application.include_router(entity_task_dependency_create)
    application.include_router(entity_task_dependency_update)
    application.include_router(entity_task_dependency_delete)
    application.include_router(entity_resource_reservation_list)
    application.include_router(entity_resource_reservation_get)
    application.include_router(entity_resource_reservation_create)
    application.include_router(entity_resource_reservation_update)
    application.include_router(entity_resource_reservation_delete)
    application.include_router(entity_ingredient_total_list)
    application.include_router(entity_ingredient_total_get)
    application.include_router(entity_pantry_lot_list)
    application.include_router(entity_pantry_lot_get)
    application.include_router(entity_pantry_lot_create)
    application.include_router(entity_pantry_lot_update)
    application.include_router(entity_pantry_lot_delete)
    application.include_router(entity_shopping_item_list)
    application.include_router(entity_shopping_item_get)
    application.include_router(entity_shopping_item_create)
    application.include_router(entity_shopping_item_update)
    application.include_router(entity_shopping_item_delete)
    application.include_router(entity_audit_event_list)
    application.include_router(entity_audit_event_get)
    application.include_router(entity_outbox_event_list)
    application.include_router(entity_outbox_event_get)
    application.include_router(entity_product_preparation_rule_list)
    application.include_router(entity_product_preparation_rule_get)
    application.include_router(entity_product_preparation_rule_create)
    application.include_router(entity_food_identity_list)
    application.include_router(entity_food_identity_get)
    application.include_router(entity_food_identity_create)
    application.include_router(entity_food_identity_member_list)
    application.include_router(entity_food_identity_member_get)
    application.include_router(entity_food_identity_member_create)
    application.include_router(entity_generation_template_list)
    application.include_router(entity_generation_template_get)
    application.include_router(entity_generation_template_create)
    application.include_router(entity_generation_shard_list)
    application.include_router(entity_generation_shard_get)
    application.include_router(entity_generation_shard_create)
    application.include_router(entity_candidate_attempt_list)
    application.include_router(entity_candidate_attempt_get)
    application.include_router(entity_candidate_attempt_create)
    application.include_router(entity_candidate_attempt_update)
    application.include_router(entity_recipe_search_document_list)
    application.include_router(entity_recipe_search_document_get)
    application.include_router(entity_recipe_embedding_list)
    application.include_router(entity_recipe_embedding_get)
    application.include_router(entity_recipe_embedding_create)
    application.include_router(entity_recipe_embedding_update)
    application.include_router(entity_generation_stratum_metric_list)
    application.include_router(entity_generation_stratum_metric_get)
    application.include_router(entity_generation_stratum_metric_create)
    application.include_router(entity_receipt_import_list)
    application.include_router(entity_receipt_import_get)
    application.include_router(entity_receipt_import_create)
    application.include_router(entity_receipt_import_update)
    application.include_router(entity_receipt_import_delete)
    application.include_router(entity_receipt_line_list)
    application.include_router(entity_receipt_line_get)
    application.include_router(entity_receipt_line_create)
    application.include_router(entity_receipt_line_update)
    application.include_router(entity_receipt_line_delete)
    application.include_router(entity_workspace_revision_list)
    application.include_router(entity_workspace_revision_get)
    application.include_router(entity_user_food_list)
    application.include_router(entity_user_food_get)
    application.include_router(entity_user_food_create)
    application.include_router(entity_user_food_update)
    application.include_router(entity_user_food_delete)
    application.include_router(entity_user_pantry_food_list)
    application.include_router(entity_user_pantry_food_get)
    application.include_router(entity_user_pantry_food_create)
    application.include_router(entity_user_pantry_food_update)
    application.include_router(entity_user_pantry_food_delete)
    application.include_router(entity_pantry_consumption_list)
    application.include_router(entity_pantry_consumption_get)
    application.include_router(entity_user_shopping_check_list)
    application.include_router(entity_user_shopping_check_get)
    application.include_router(entity_user_shopping_check_create)
    application.include_router(entity_user_shopping_check_update)
    application.include_router(entity_user_shopping_check_delete)
    application.include_router(entity_backup_artifact_list)
    application.include_router(entity_backup_artifact_get)
    application.include_router(entity_backup_restore_intent_list)
    application.include_router(entity_backup_restore_intent_get)
    register_generation_routes(application)
