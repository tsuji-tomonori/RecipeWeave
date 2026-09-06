# サービス実装由来の設計

生成元: OpenAPI・TypeScript/Python実装・SQL・サンプルJSON・CDK合成結果。手編集禁止。
`uv run python tools/generate_service_design.py` で生成、`--check` で差分検査。
コードと配備定義の存在を示す。実配備・実機評価・OCR精度の実測を証明するものではない。

## 再現用の旧サンプル入力

食材 35 件、料理 8 件。初期検証に用いた標本。公開APIの実データ取得元は各SQL仕様、正規化DBへの投入はdatabase/seed.pyを参照する。

| ファイル | SHA-256 |
|---|---|
| `data/samples/foods.json` | `69f10ea50bc80682b9bbfd5613fc749584bc78c3dd50a58bc2ddfe6f429f940c` |
| `data/samples/recipes.json` | `cd12f4aa81a30967fd9485b1d0218727ec87f89a2a6151b0bda06ed1a34412c7` |

## API

| Method | Path | operationId | 認証定義 | 応答 |
|---|---|---|---|---|
| POST | `/api/auth/local-login` | `local_login` | 公開 | 200, 401, 404, 422, 503 |
| POST | `/api/backups/export` | `export_backup` | HTTPBearer | 200, 401, 403, 409, 413, 422, 503 |
| POST | `/api/backups/preview` | `preview_backup` | HTTPBearer | 200, 401, 403, 409, 413, 422, 503 |
| POST | `/api/backups/restore` | `restore_backup` | HTTPBearer | 200, 401, 403, 409, 413, 422, 503 |
| POST | `/api/cooking-plan` | `preview_cooking_plan` | HTTPBearer | 200, 401, 403, 404, 422, 503 |
| POST | `/api/cooking-sessions` | `create_cooking_session` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PATCH | `/api/cooking-sessions/{row_id}` | `update_cooking_session` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/allergen` | `entity_allergen_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/allergen` | `entity_allergen_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/allergen/{row_id}` | `entity_allergen_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/allergen/{row_id}` | `entity_allergen_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/app_user` | `entity_app_user_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| GET | `/api/entities/app_user/{row_id}` | `entity_app_user_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/app_user/{row_id}` | `entity_app_user_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/audit_event` | `entity_audit_event_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| GET | `/api/entities/audit_event/{row_id}` | `entity_audit_event_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/axis` | `entity_axis_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/axis` | `entity_axis_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/axis/{row_id}` | `entity_axis_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/axis/{row_id}` | `entity_axis_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/axis_option` | `entity_axis_option_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/axis_option` | `entity_axis_option_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/axis_option/{row_id}` | `entity_axis_option_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/axis_option/{row_id}` | `entity_axis_option_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/backup_artifact` | `entity_backup_artifact_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| GET | `/api/entities/backup_artifact/{row_id}` | `entity_backup_artifact_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/backup_restore_intent` | `entity_backup_restore_intent_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| GET | `/api/entities/backup_restore_intent/{row_id}` | `entity_backup_restore_intent_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/candidate_attempt` | `entity_candidate_attempt_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/candidate_attempt` | `entity_candidate_attempt_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/candidate_attempt/{row_id}` | `entity_candidate_attempt_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/candidate_attempt/{row_id}` | `entity_candidate_attempt_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/catalog_release` | `entity_catalog_release_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/catalog_release` | `entity_catalog_release_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/catalog_release/{row_id}` | `entity_catalog_release_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/catalog_release/{row_id}` | `entity_catalog_release_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/compatibility_rule` | `entity_compatibility_rule_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/compatibility_rule` | `entity_compatibility_rule_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/compatibility_rule/{row_id}` | `entity_compatibility_rule_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/conversion` | `entity_conversion_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/conversion` | `entity_conversion_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/conversion/{row_id}` | `entity_conversion_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/conversion/{row_id}` | `entity_conversion_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/cooking_session` | `entity_cooking_session_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/cooking_session` | `entity_cooking_session_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/cooking_session/{row_id}` | `entity_cooking_session_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/cooking_session/{row_id}` | `entity_cooking_session_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/cooking_session/{row_id}` | `entity_cooking_session_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/food` | `entity_food_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/food` | `entity_food_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/food/{row_id}` | `entity_food_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/food/{row_id}` | `entity_food_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/food_alias` | `entity_food_alias_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/food_alias` | `entity_food_alias_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/food_alias/{row_id}` | `entity_food_alias_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/food_alias/{row_id}` | `entity_food_alias_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/food_allergen` | `entity_food_allergen_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/food_allergen` | `entity_food_allergen_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/food_allergen/{row_id}` | `entity_food_allergen_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/food_axis_option` | `entity_food_axis_option_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/food_axis_option` | `entity_food_axis_option_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/food_axis_option/{row_id}` | `entity_food_axis_option_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/food_axis_option/{row_id}` | `entity_food_axis_option_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/food_form` | `entity_food_form_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/food_form` | `entity_food_form_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/food_form/{row_id}` | `entity_food_form_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/food_form/{row_id}` | `entity_food_form_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/food_identity` | `entity_food_identity_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/food_identity` | `entity_food_identity_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/food_identity/{row_id}` | `entity_food_identity_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/food_identity_member` | `entity_food_identity_member_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/food_identity_member` | `entity_food_identity_member_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/food_identity_member/{row_id}` | `entity_food_identity_member_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/form_yield` | `entity_form_yield_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/form_yield` | `entity_form_yield_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/form_yield/{row_id}` | `entity_form_yield_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/generation_choice` | `entity_generation_choice_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/generation_choice` | `entity_generation_choice_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/generation_choice/{row_id}` | `entity_generation_choice_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/generation_choice/{row_id}` | `entity_generation_choice_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/generation_food` | `entity_generation_food_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/generation_food` | `entity_generation_food_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/generation_food/{row_id}` | `entity_generation_food_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/generation_food/{row_id}` | `entity_generation_food_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/generation_job` | `entity_generation_job_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/generation_job` | `entity_generation_job_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/generation_job/{row_id}` | `entity_generation_job_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/generation_job/{row_id}` | `entity_generation_job_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/generation_policy` | `entity_generation_policy_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/generation_policy` | `entity_generation_policy_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/generation_policy/{row_id}` | `entity_generation_policy_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/generation_result` | `entity_generation_result_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/generation_result` | `entity_generation_result_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/generation_result/{row_id}` | `entity_generation_result_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/generation_shard` | `entity_generation_shard_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/generation_shard` | `entity_generation_shard_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/generation_shard/{row_id}` | `entity_generation_shard_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/generation_stratum_metric` | `entity_generation_stratum_metric_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/generation_stratum_metric` | `entity_generation_stratum_metric_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/generation_stratum_metric/{row_id}` | `entity_generation_stratum_metric_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/generation_template` | `entity_generation_template_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/generation_template` | `entity_generation_template_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/generation_template/{row_id}` | `entity_generation_template_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/ingredient_total` | `entity_ingredient_total_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| GET | `/api/entities/ingredient_total/{row_id}` | `entity_ingredient_total_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/kitchen_resource` | `entity_kitchen_resource_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/kitchen_resource` | `entity_kitchen_resource_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/kitchen_resource/{row_id}` | `entity_kitchen_resource_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/kitchen_resource/{row_id}` | `entity_kitchen_resource_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/kitchen_resource/{row_id}` | `entity_kitchen_resource_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/material_node` | `entity_material_node_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/material_node` | `entity_material_node_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/material_node/{row_id}` | `entity_material_node_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/material_node/{row_id}` | `entity_material_node_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/media_asset` | `entity_media_asset_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/media_asset` | `entity_media_asset_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/media_asset/{row_id}` | `entity_media_asset_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/menu` | `entity_menu_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/menu` | `entity_menu_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/menu/{row_id}` | `entity_menu_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/menu/{row_id}` | `entity_menu_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/menu/{row_id}` | `entity_menu_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/menu_ingredient_override` | `entity_menu_ingredient_override_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/menu_ingredient_override` | `entity_menu_ingredient_override_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/menu_ingredient_override/{row_id}` | `entity_menu_ingredient_override_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/menu_ingredient_override/{row_id}` | `entity_menu_ingredient_override_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/menu_ingredient_override/{row_id}` | `entity_menu_ingredient_override_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/menu_item` | `entity_menu_item_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/menu_item` | `entity_menu_item_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/menu_item/{row_id}` | `entity_menu_item_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/menu_item/{row_id}` | `entity_menu_item_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/menu_item/{row_id}` | `entity_menu_item_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/nutrient` | `entity_nutrient_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/nutrient` | `entity_nutrient_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/nutrient/{row_id}` | `entity_nutrient_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/nutrient/{row_id}` | `entity_nutrient_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/nutrition_fact` | `entity_nutrition_fact_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/nutrition_fact` | `entity_nutrition_fact_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/nutrition_fact/{row_id}` | `entity_nutrition_fact_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/operation` | `entity_operation_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/operation` | `entity_operation_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/operation/{row_id}` | `entity_operation_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/operation/{row_id}` | `entity_operation_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/operation_parameter` | `entity_operation_parameter_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/operation_parameter` | `entity_operation_parameter_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/operation_parameter/{row_id}` | `entity_operation_parameter_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/operation_parameter/{row_id}` | `entity_operation_parameter_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/outbox_event` | `entity_outbox_event_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| GET | `/api/entities/outbox_event/{row_id}` | `entity_outbox_event_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/pantry_consumption` | `entity_pantry_consumption_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| GET | `/api/entities/pantry_consumption/{row_id}` | `entity_pantry_consumption_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/pantry_lot` | `entity_pantry_lot_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/pantry_lot` | `entity_pantry_lot_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/pantry_lot/{row_id}` | `entity_pantry_lot_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/pantry_lot/{row_id}` | `entity_pantry_lot_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/pantry_lot/{row_id}` | `entity_pantry_lot_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/product` | `entity_product_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/product` | `entity_product_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/product/{row_id}` | `entity_product_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/product/{row_id}` | `entity_product_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/product_allergen` | `entity_product_allergen_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/product_allergen` | `entity_product_allergen_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/product_allergen/{row_id}` | `entity_product_allergen_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/product_component` | `entity_product_component_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/product_component` | `entity_product_component_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/product_component/{row_id}` | `entity_product_component_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/product_preparation_rule` | `entity_product_preparation_rule_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/product_preparation_rule` | `entity_product_preparation_rule_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/product_preparation_rule/{row_id}` | `entity_product_preparation_rule_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/product_version` | `entity_product_version_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/product_version` | `entity_product_version_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/product_version/{row_id}` | `entity_product_version_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/receipt_import` | `entity_receipt_import_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/receipt_import` | `entity_receipt_import_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/receipt_import/{row_id}` | `entity_receipt_import_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/receipt_import/{row_id}` | `entity_receipt_import_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/receipt_import/{row_id}` | `entity_receipt_import_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/receipt_line` | `entity_receipt_line_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/receipt_line` | `entity_receipt_line_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/receipt_line/{row_id}` | `entity_receipt_line_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/receipt_line/{row_id}` | `entity_receipt_line_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/receipt_line/{row_id}` | `entity_receipt_line_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/recipe` | `entity_recipe_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/recipe` | `entity_recipe_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/recipe/{row_id}` | `entity_recipe_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/recipe/{row_id}` | `entity_recipe_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/recipe_embedding` | `entity_recipe_embedding_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/recipe_embedding` | `entity_recipe_embedding_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/recipe_embedding/{row_id}` | `entity_recipe_embedding_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/recipe_embedding/{row_id}` | `entity_recipe_embedding_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/recipe_ingredient` | `entity_recipe_ingredient_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/recipe_ingredient` | `entity_recipe_ingredient_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/recipe_ingredient/{row_id}` | `entity_recipe_ingredient_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/recipe_ingredient/{row_id}` | `entity_recipe_ingredient_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/recipe_option` | `entity_recipe_option_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/recipe_option` | `entity_recipe_option_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/recipe_option/{row_id}` | `entity_recipe_option_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/recipe_option/{row_id}` | `entity_recipe_option_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/recipe_search_document` | `entity_recipe_search_document_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| GET | `/api/entities/recipe_search_document/{row_id}` | `entity_recipe_search_document_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/recipe_signature` | `entity_recipe_signature_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/recipe_signature` | `entity_recipe_signature_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/recipe_signature/{row_id}` | `entity_recipe_signature_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/recipe_similarity` | `entity_recipe_similarity_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/recipe_similarity` | `entity_recipe_similarity_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/recipe_similarity/{row_id}` | `entity_recipe_similarity_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/recipe_similarity/{row_id}` | `entity_recipe_similarity_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/recipe_step` | `entity_recipe_step_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/recipe_step` | `entity_recipe_step_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/recipe_step/{row_id}` | `entity_recipe_step_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/recipe_step/{row_id}` | `entity_recipe_step_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/recipe_version` | `entity_recipe_version_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/recipe_version` | `entity_recipe_version_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/recipe_version/{row_id}` | `entity_recipe_version_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/recipe_version/{row_id}` | `entity_recipe_version_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/resource_reservation` | `entity_resource_reservation_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/resource_reservation` | `entity_resource_reservation_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/resource_reservation/{row_id}` | `entity_resource_reservation_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/resource_reservation/{row_id}` | `entity_resource_reservation_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/resource_reservation/{row_id}` | `entity_resource_reservation_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/resource_type` | `entity_resource_type_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/resource_type` | `entity_resource_type_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/resource_type/{row_id}` | `entity_resource_type_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/resource_type/{row_id}` | `entity_resource_type_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/scaling_point` | `entity_scaling_point_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/scaling_point` | `entity_scaling_point_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/scaling_point/{row_id}` | `entity_scaling_point_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/scaling_rule` | `entity_scaling_rule_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/scaling_rule` | `entity_scaling_rule_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/scaling_rule/{row_id}` | `entity_scaling_rule_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/session_task` | `entity_session_task_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/session_task` | `entity_session_task_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/session_task/{row_id}` | `entity_session_task_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/session_task/{row_id}` | `entity_session_task_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/session_task/{row_id}` | `entity_session_task_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/shopping_item` | `entity_shopping_item_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/shopping_item` | `entity_shopping_item_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/shopping_item/{row_id}` | `entity_shopping_item_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/shopping_item/{row_id}` | `entity_shopping_item_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/shopping_item/{row_id}` | `entity_shopping_item_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/source_record` | `entity_source_record_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/source_record` | `entity_source_record_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/source_record/{row_id}` | `entity_source_record_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/source_record/{row_id}` | `entity_source_record_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/step_dependency` | `entity_step_dependency_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/step_dependency` | `entity_step_dependency_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/step_dependency/{row_id}` | `entity_step_dependency_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/step_dependency/{row_id}` | `entity_step_dependency_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/step_input` | `entity_step_input_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/step_input` | `entity_step_input_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/step_input/{row_id}` | `entity_step_input_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/step_input/{row_id}` | `entity_step_input_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/step_media` | `entity_step_media_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/step_media` | `entity_step_media_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/step_media/{row_id}` | `entity_step_media_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/step_media/{row_id}` | `entity_step_media_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/step_parameter` | `entity_step_parameter_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/step_parameter` | `entity_step_parameter_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/step_parameter/{row_id}` | `entity_step_parameter_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/step_parameter/{row_id}` | `entity_step_parameter_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/step_resource` | `entity_step_resource_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/step_resource` | `entity_step_resource_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/step_resource/{row_id}` | `entity_step_resource_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/step_resource/{row_id}` | `entity_step_resource_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/task_dependency` | `entity_task_dependency_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/task_dependency` | `entity_task_dependency_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/task_dependency/{row_id}` | `entity_task_dependency_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/task_dependency/{row_id}` | `entity_task_dependency_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/task_dependency/{row_id}` | `entity_task_dependency_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/unit` | `entity_unit_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/unit` | `entity_unit_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/unit/{row_id}` | `entity_unit_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/unit/{row_id}` | `entity_unit_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/user_exclusion` | `entity_user_exclusion_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/user_exclusion` | `entity_user_exclusion_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/user_exclusion/{row_id}` | `entity_user_exclusion_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/user_exclusion/{row_id}` | `entity_user_exclusion_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/user_exclusion/{row_id}` | `entity_user_exclusion_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/user_food` | `entity_user_food_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/user_food` | `entity_user_food_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/user_food/{row_id}` | `entity_user_food_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/user_food/{row_id}` | `entity_user_food_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/user_food/{row_id}` | `entity_user_food_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/user_pantry_food` | `entity_user_pantry_food_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/user_pantry_food` | `entity_user_pantry_food_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/user_pantry_food/{row_id}` | `entity_user_pantry_food_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/user_pantry_food/{row_id}` | `entity_user_pantry_food_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/user_pantry_food/{row_id}` | `entity_user_pantry_food_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/user_preference` | `entity_user_preference_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/user_preference` | `entity_user_preference_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/user_preference/{row_id}` | `entity_user_preference_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/user_preference/{row_id}` | `entity_user_preference_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/user_preference/{row_id}` | `entity_user_preference_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/user_recipe_event` | `entity_user_recipe_event_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/user_recipe_event` | `entity_user_recipe_event_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/user_recipe_event/{row_id}` | `entity_user_recipe_event_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/user_recipe_event/{row_id}` | `entity_user_recipe_event_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/user_shopping_check` | `entity_user_shopping_check_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/user_shopping_check` | `entity_user_shopping_check_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| DELETE | `/api/entities/user_shopping_check/{row_id}` | `entity_user_shopping_check_delete` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/user_shopping_check/{row_id}` | `entity_user_shopping_check_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/entities/user_shopping_check/{row_id}` | `entity_user_shopping_check_update` | HTTPBearer | 200, 401, 403, 409, 422, 428, 503 |
| GET | `/api/entities/validation_result` | `entity_validation_result_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| POST | `/api/entities/validation_result` | `entity_validation_result_create` | HTTPBearer | 201, 401, 403, 409, 422, 503 |
| GET | `/api/entities/validation_result/{row_id}` | `entity_validation_result_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/entities/workspace_revision` | `entity_workspace_revision_list` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| GET | `/api/entities/workspace_revision/{row_id}` | `entity_workspace_revision_get` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/foods` | `list_foods` | HTTPBearer | 200, 401, 422, 503 |
| POST | `/api/foods/custom` | `create_custom_food` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| POST | `/api/generation/shards/claim` | `claim_shard` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| PUT | `/api/generation/shards/{row_id}/lease` | `renew_shard` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| PUT | `/api/generation/shards/{row_id}/progress` | `advance_shard` | HTTPBearer | 200, 401, 403, 409, 422, 503 |
| GET | `/api/health` | `get_health` | 公開 | 200 |
| GET | `/api/me` | `get_me` | HTTPBearer | 200, 401, 404, 422, 503 |
| POST | `/api/menus/current/items` | `add_menu_item` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| DELETE | `/api/menus/current/items/{row_id}` | `delete_menu_item` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PATCH | `/api/menus/current/items/{row_id}` | `update_menu_item` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| POST | `/api/pantry-lots` | `create_pantry_lot` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| DELETE | `/api/pantry-lots/{row_id}` | `delete_pantry_lot` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PATCH | `/api/pantry-lots/{row_id}` | `update_pantry_lot` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| POST | `/api/receipts/commit` | `commit_receipt` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| POST | `/api/receipts/{row_id}/undo` | `undo_receipt` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/recipes` | `list_recipes` | HTTPBearer | 200, 401, 403, 422, 503 |
| GET | `/api/recipes/random` | `random_recipe` | HTTPBearer | 200, 401, 403, 422, 503 |
| GET | `/api/recipes/{recipe_id}` | `get_recipe` | HTTPBearer | 200, 401, 403, 404, 422, 503 |
| DELETE | `/api/saved-recipes/{row_id}` | `unsave_recipe` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/saved-recipes/{row_id}` | `save_recipe` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/settings` | `put_settings` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| PUT | `/api/shopping-checks` | `put_shopping_checks` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |
| GET | `/api/workspace` | `get_workspace` | HTTPBearer | 200, 401, 403, 404, 409, 422, 503 |

## 実装の公開要素

| ファイル | 公開要素 | SHA-256 |
|---|---|---|
| `frontend/src/App.test.ts` | 検証コード | `237e51869d611439a320ce6321f67075231ea1508049405805522b1933b6b2dd` |
| `frontend/src/lib/api-contract.ts` | `WorkspaceResponse`, `RevisionRequest`, `WorkspaceMutationResponse`, `CreatePantryLotRequest`, `UpdatePantryLotRequest`, `CommitReceiptRequest`, `AddMenuItemRequest`, `PutSettingsRequest`, `PutShoppingChecksRequest`, `CreateCookingSessionRequest`, `UpdateCookingSessionRequest`, `PreviewCookingPlanRequest`, `PreviewCookingPlanResponse`, `CreateCustomFoodRequest` | `cd1a70967466360896a5767d90a7bfaacf364d53439bd0e2ed1c9124880602d3` |
| `frontend/src/lib/api.test.ts` | 検証コード | `c821f222704d51e54f938e0caed8eb371b33bcd7e26130c5974c3a485390aa78` |
| `frontend/src/lib/api.ts` | `User`, `StateEnvelope`, `RecipePage`, `ApiError`, `request`, `localLogin`, `currentUser`, `loadFoods`, `findRecipes`, `randomRecipe`, `loadRecipe`, `loadState`, `saveState`, `completeCooking`, `commitReceipt`, `previewCookingPlan`, `exportDatabaseBackup`, `previewDatabaseBackup`, `restoreDatabaseBackup` | `eadd31beb4fdd8fd9c2d3cc2ed9942a2a7cd69a3a24d4b2001fa39b4ccceb2c7` |
| `frontend/src/lib/auth.test.ts` | 検証コード | `007954eb06b22ad583e0f707501254830bb19c2f471ecb027091de90d258e586` |
| `frontend/src/lib/auth.ts` | `localMode`, `getToken`, `setToken`, `clearToken`, `loginCognito`, `completeLogin`, `logout` | `1beef8d3417207cc4b5a8723dde17df38408e5b7072529cc5e7c5d98eac74a69` |
| `frontend/src/lib/backup.test.ts` | 検証コード | `77efde125939de9173ad9b6c0edafb0fbf86b2ac441d7b55cdf88455c35be9f7` |
| `frontend/src/lib/backup.ts` | `MAX_BACKUP_BYTES`, `BackupInput`, `BackupPreview`, `readBackupFile` | `1f548e6fd07931468623f1135f91ac72b9cd553273dcadf4aecb7c2074e615aa` |
| `frontend/src/lib/catalog-contract.test.ts` | 検証コード | `a5380ab72d1d6c7cc8b77a8ac7bee26a47f24b8c6a74be3bdf85b0344086869c` |
| `frontend/src/lib/domain.test.ts` | 検証コード | `05077452f7c0ef12e476e084678f3db16e96811fe19a30181d10a045eda8353e` |
| `frontend/src/lib/domain.ts` | `FOODS`, `RECIPES`, `setCatalog`, `cacheRecipes`, `DomainError`, `newId`, `validateQuantity`, `createInitialState`, `allFoods`, `getFood`, `getRecipe`, `quantityText`, `ingredientKey`, `getDraft`, `scaleDraft`, `setDraftAmount`, `saveDraft`, `resetDraft`, `addToMeal`, `updateMeal`, `removeFromMeal`, `toggleSaved`, `addCustomFood`, `addStock`, `updateStock`, `deleteStock`, `restoreStock`, `duplicateImports`, `commitReceipt`, `previewUndoImport`, `undoImport`, `requiredQuantities`, `shoppingList`, `toggleShoppingCheck`, `searchRecipes`, `randomRecipe`, `arrangements`, `buildCookingPlan`, `startCooking`, `moveCooking`, `pauseCooking`, `resumeCooking`, `startTimer`, `timerRemaining`, `previewConsumption`, `completeCooking` | `146af9c0a7f055e52243e9e0965d84face2aeb8372e6d5331b15601a0b8e3c23` |
| `frontend/src/lib/ocr.ts` | `OcrTask`, `validateReceiptImage`, `recognizeReceipt` | `e017bc1ff238edf30fe43b440752cd66c70d45172ad73bf3f9687b37947efeab` |
| `frontend/src/lib/persistence.ts` | `STORAGE_KEY`, `StorageLike`, `LockManagerLike`, `RecoverySnapshot`, `validateAppState`, `parseBackup`, `loadState`, `inspectRecovery`, `transact`, `exportBackup`, `restoreBackup`, `recoverBackup` | `38e94de450ae9f4f6a2f972eca49e4cbf050df3988c88294bfc1e31f117db338` |
| `frontend/src/lib/receipt.ts` | `parseReceipt`, `receiptSignature`, `validateReceiptFile`, `hashImage` | `293c705dfc2f47b9657deffb4123bcb00a4056693520648ef75df5f9ed3e4c53` |
| `frontend/src/lib/types.ts` | `UNITS`, `Unit`, `StorageLocation`, `Quantity`, `Food`, `RecipeIngredient`, `TimeScalingMode`, `DurationEstimate`, `RecipeStep`, `Recipe`, `RecipeDraft`, `MealItem`, `StockLot`, `ReceiptImport`, `ReceiptCandidate`, `ReceiptCommit`, `ShoppingCheck`, `ShoppingRow`, `ShoppingList`, `PlannedStep`, `CookingTimer`, `ConsumptionRequest`, `ConsumptionResult`, `CookingSession`, `Settings`, `SearchFilters`, `AppState`, `StockInput`, `UndoPreview` | `bc07fc8746fe109e30c585bc2b53256442c70d9972e5e81bfa22ce336444ffc2` |
| `frontend/src/main.ts` | 画面コンポーネント／起動処理 | `ec315a1d373f5470b11a7dcaa0d972ab81e3f513113325bd18aea471c1ce2d62` |
| `frontend/src/test-fixtures.ts` | `fixtureFoods`, `fixtureRecipes` | `7898608c422027651efb2521013d31dfdeb59d78cd50cd7a53bd90853a45e178` |
| `frontend/src/App.svelte` | 画面コンポーネント／起動処理 | `10ae312c167c513c70519942fe5630f6cce5fceb71757f5a7081fdad4882c70e` |
| `frontend/src/lib/FoodSettings.svelte` | 画面コンポーネント／起動処理 | `a812bfc75e03bf4b82c1dae1b46b765c1db19640456eed86b6518aa34dd662c7` |
| `frontend/src/lib/FoodTile.svelte` | 画面コンポーネント／起動処理 | `8be1fc4f7ab1b54c026a7ff77fa74f67e479f8b09a7cf25c944807da71024333` |
| `frontend/src/lib/RecipeCard.svelte` | 画面コンポーネント／起動処理 | `04bb0c6df673eacfba6aeeba92df6092dd54ec1f09af471114cf53186c7a6ace` |

## SQL境界

| SQL | SHA-256 |
|---|---|
| `backend/src/app/apis/auth/get_me/sql/q001_set_identity.sql` | `c2f251fde20a71176edddfff94e99504b1b0fba96a623f1b62cc8fe4dc640f15` |
| `backend/src/app/apis/auth/get_me/sql/q002_initialize_user.sql` | `d2fa642225748bf955a9a8dc26c111286aa9fa1747ded61275070e6cd10ee4bc` |
| `backend/src/app/apis/auth/get_me/sql/q003_select_user.sql` | `4ded63ca08f484bd5b5cbcac75da9a9426efefd31bb870bb67d887d586a703e3` |
| `backend/src/app/apis/auth/get_me/sql/q004_initialize_revision.sql` | `321b6f7464e8c8f4e14763b26a0d39b5bb98394e03543170bf2fd574ee86067f` |
| `backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql` | `c89b36ed13995b8e6de523b856446e6b79917067b9c940e5fbf5efd9ae1620b4` |
| `backend/src/app/apis/backup/export_backup/sql/q001_lock_revision.sql` | `28c2f7fec63fdc8a39f44e0e25d68b8eaa0e0ddb7d99a918e04af3234143ef0e` |
| `backend/src/app/apis/backup/export_backup/sql/q002_profile.sql` | `49f6e17337f7645e036792de082a441de70b9cba6ef89f80229e5f4e72852ad5` |
| `backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql` | `703a6c33c9a8598c3c37c5b39cf22ff286c28ca50b82dac89c9a7571d0ae89a4` |
| `backend/src/app/apis/backup/export_backup/sql/q021_issue_artifact.sql` | `5fd3d30092889c82af9b6dff50a7d93242b9a6464be0b765d6917625fa4ea7bb` |
| `backend/src/app/apis/backup/preview_backup/sql/q001_lock_revision.sql` | `28c2f7fec63fdc8a39f44e0e25d68b8eaa0e0ddb7d99a918e04af3234143ef0e` |
| `backend/src/app/apis/backup/preview_backup/sql/q002_profile.sql` | `49f6e17337f7645e036792de082a441de70b9cba6ef89f80229e5f4e72852ad5` |
| `backend/src/app/apis/backup/preview_backup/sql/q010_export_tables.sql` | `703a6c33c9a8598c3c37c5b39cf22ff286c28ca50b82dac89c9a7571d0ae89a4` |
| `backend/src/app/apis/backup/preview_backup/sql/q020_artifact.sql` | `b9c8654dc89a48abfcefb7739c1e61d0ba399e82ff618c4f89cc25ea62716066` |
| `backend/src/app/apis/backup/preview_backup/sql/q022_issue_intent.sql` | `cfc6818fceac6db3aff49e4b81f3f443a85249cf507e827524887f4bdbbc32f8` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_catalog_release.sql` | `788fe9694659105cd7b588769f5a8ba6862f5de0604b10721f10d87025f4c336` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_conversion.sql` | `2516b98959e3210c4d77616794b738b423001e4864f647c5345c140efce370d2` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_cooking_session.sql` | `e4c418e253845c782b4eb5772c94ba4fd3a3d9a7be76f2059bb696398f1ab633` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_food.sql` | `e9a343d27f6b16090d78cffc070593b32a6917b7fb7132d9b4858ca02d4fa10b` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_food_alias.sql` | `76f6f6044cdef4be3eb8ba91cc956f3346e7f987a820c59bee74621bc58aa3b0` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_food_allergen.sql` | `202d65291f9a1e9fa01eceb8de32e47ea448463545f296d385aca5b17b5ead4f` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_food_axis_option.sql` | `006d271d9c423fdd0c37edd6ecdbd8c97b15e8cfe46c66c95663e0869c6f016a` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_food_form.sql` | `f04b7465cf8ebbac28e7b706445178dc284933b2758661630fd05e72c71e8170` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_form_yield.sql` | `af108757889088ab842e5054118836464d81dd5da5c1f6d7b804d88bf9930e78` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_ingredient_total.sql` | `7363d86e7820182d4b7f3ea6a572a8faed8c291db93a6dc605ee6d0374ea3aed` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_kitchen_resource.sql` | `ac62a77fe15bc324ba70014344bd3d8a5195f1663f08d7239cd034958a3f0a63` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_menu.sql` | `60d9ff3ddf5d79ff32375683030a8b6250c86b48b75eab96553fe830a039ae77` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_menu_ingredient_override.sql` | `be4cc85b407ed4a6af2865a3d8f485407568f28578949bd39902ca63889a0c33` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_menu_item.sql` | `9b5e1b93cbed61140e86c5d3a04c9a26bdb66a3f1b7c2d14040abcfaf8ae224a` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_nutrition_fact.sql` | `87ca137f255f586bd1ce4b1d1177a4165d44d8f02b0157c5dfbaa82b2117182c` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_pantry_consumption.sql` | `ebeb195f39ba31e57b9467248210e05bc188f48880e7d06e5a59de6b4e60e6df` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_pantry_lot.sql` | `f921c2830d9357c08133f2a9ae03e3e766e165e004512a99478afc758976ef33` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_product.sql` | `2e865c898fef1379cb0fc82c3b637ba957a6322bcccb42b049eb3886514ea801` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_product_allergen.sql` | `ba2b3415f02205c1f51a19d98a1cbff187c4dfb3f35577cf57548fe0767e0367` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_product_component.sql` | `2f916276269a6ee05f44926ea784267836abc1f1575e583082f1f1dad6faea9e` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_product_preparation_rule.sql` | `078fdb27cc7cdf3e19b7a716076b59dcfe1d080aba0f01cf0b7cdb0ae132cdfd` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_product_version.sql` | `6cfc27ac259e1c0d0e74ef7fc69248c4b41d746225789f43c56f8d916875f046` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_receipt_import.sql` | `c848381ee7747c602bd757c29d3e4f12f0e2eca70adf8d405f031cbf92d74717` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_receipt_line.sql` | `3bc87b431b8a29e2c586a2f44afa7d1b2828c6c711bc9c43619c47b5529dd586` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_resource_reservation.sql` | `4640a373130076eaa621ce59b410b01730c13575c0e1031d8820b36bd0d2910f` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_session_task.sql` | `851e7575e5b72a1b45a014e9812f6eaa5a5ef1e96a5cdafc3367223e0c9f804b` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_shopping_item.sql` | `56d08128e320d50c9aadffe0b74734f67068a14e38b37aa00693781b4db0cc62` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_task_dependency.sql` | `8157207df1ff85c0f600177ef8dbb367369b47a1b6d52a02a18e1f9327599175` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_user_exclusion.sql` | `2964224c329b3533669afa23b957c329da4ee069664a999f1efea0065bc1253c` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_user_food.sql` | `921a4cbbf72531bde25180066e67bd7050deafb69ccc55e917168e662c69664a` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_user_pantry_food.sql` | `6278d4a828b1d2b9c9515bdd100336dcdc9738181412871c3045d6a583bdb101` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_user_preference.sql` | `17b30d4baa5717188a88947d0a280186f9ad9da1a52ebf601fc74f098e041beb` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_user_recipe_event.sql` | `70e16a4f267c48b48c2edc74326d982827e307aba1e1a3876dbc7ad8bdb9831e` |
| `backend/src/app/apis/backup/preview_backup/sql/q100_delete_user_shopping_check.sql` | `b6e692637d7bfa0d1bfa9f0d195a6783e01b67583eaf1c0a116d5b94ac0e6ea2` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_catalog_release.sql` | `1f5222a09e4a70b71a23b52c188a945e254db08e50c417de076c8a4bcd8cdfe1` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_conversion.sql` | `cc7e8e2dc6b4dccbdccde79df89ea34c4434a0c77d482155086a3a9445b29224` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_cooking_session.sql` | `7259c2c2e35b584f332510c5e5ba01dd637f349154bd064b20c8872b0150b9a1` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_food.sql` | `ad70bf20fe116835c5fc9969893156918077695a618a0b69e2ed9fba5656e2dc` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_food_alias.sql` | `55a379b5eb0b50d277c1c4c79c2f3aaf7b34ca8f913e4ff82663125ee38c1b3d` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_food_allergen.sql` | `14f3b992c02eced61448184d7ae6bbb669101137264c7cc1b9b0e8ef59b03a1a` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_food_axis_option.sql` | `a24e3bb094def0d08b21aa15e7d2bc71394b01b69ab07b768aba0714c6a08a3a` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_food_form.sql` | `e5a35d8dc2d7e28f80ccf56043b671d79f700d3176b6e1ef316ebca1183932a1` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_form_yield.sql` | `dd79fdde086814b1b2f7e4c6b63b71dca95f0454200be41aceba7f33881bb4e6` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_ingredient_total.sql` | `70780a34840e7dbc4e6afc9027ab53853b36bee1202ebb5e9e9a7f9c3e6e320a` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_kitchen_resource.sql` | `971bce45db5ac8434c49945e86a9d5b8e3075650f8be49316c8f555f7231b22e` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_menu.sql` | `02ed6d8da195820324e78100c93a4d3a6f9b8eb897454c78f2640cf99d570e9e` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_menu_ingredient_override.sql` | `9929e63497ce75ba24b99fbcb80ad91d757a64ff558a98da4eb3e2d04ce75f7a` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_menu_item.sql` | `b6e70b517aaa1232ad887aadb37c3475439e3a9c820353640816851a46de14be` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_nutrition_fact.sql` | `6398d7736ad91430d3fc169cb2daefe6f5d437382e5e7303f59a07db6a69ba57` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_pantry_consumption.sql` | `016dea80bb179b36f08dce4ab92c94c7108cf5841529820fa7de70e944003aff` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_pantry_lot.sql` | `734629f0d3495d28399e1cc2478e01d000a39462ce262f3cf4e93a0735fd7a31` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_product.sql` | `2a9c4834b712d82c0be6e6a1691d26de88903873442aff4a9eecc79a98feee45` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_product_allergen.sql` | `5e8414ff1cb91fb1c7db95680a1f920839ebf34899635c4e13190259ecb245ef` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_product_component.sql` | `5ea2333d0e787a8106b6b2b73835659e3ef6702eeb16d780c8f3b6b758cf33c0` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_product_preparation_rule.sql` | `d6f4516420ae7edd3ca867bcaf69b6b291d0b3835a654cf4a36b67694efa3afb` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_product_version.sql` | `f00ce29801482be5cde208a41ae0cb11e84d26e98da73514c26d14e918007823` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_receipt_import.sql` | `d4c8776ffc8a32fe0a45d1bcbfb86f1be69c4ce90f6208731e842c2ee1afd694` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_receipt_line.sql` | `38b5decf1176dc6834e9b184d78d3821da39cd8e9a7f7a9267315f736641994d` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_resource_reservation.sql` | `cb98c239c7b3a3a4489edd1cc187123f1fb331ac7156905a33b291c07586d823` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_session_task.sql` | `4e2e98a536c6b1959811ecbd84ab08125f90567355826ad1ea275e508c19ea2f` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_shopping_item.sql` | `9a3ce297734d5c68e7fa233916faaf3d14b2ce6f8b5bc609404eedd3dc25ff25` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_task_dependency.sql` | `b43accae305854ac7f73e98129b91f6d9eda58aac7027734b27df2e8eca2ce2e` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_user_exclusion.sql` | `10cd7434d6262ef711c0019f6a13f6b02e944d0de5d04bbe4455ebfd1bc2a7cc` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_user_food.sql` | `413e056710325779644f9b82157b7b360fef45939c93d075f6049c41645d9d1f` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_user_pantry_food.sql` | `d476da8f6d450e9cf156870017d5bc1cc2b8c8a8db9f5317d24a5e1a82e9affc` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_user_preference.sql` | `f59939725d1999d158c70fbf795e141e8a8528721e59540005913f491947f824` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_user_recipe_event.sql` | `cbabe82ebbd9099e5410e4f5e8df98f33df6b87703e1be2e55dccd0bfa524d9c` |
| `backend/src/app/apis/backup/preview_backup/sql/q200_insert_user_shopping_check.sql` | `bfa815ee6e75d46f3b0754fa7edf178538337f3ebc54bd88633879926d29a680` |
| `backend/src/app/apis/backup/preview_backup/sql/q300_reference_allergen.sql` | `0ea865de5e1030261ae49250e80e5b491133d6f6974797254e31d22969e03f06` |
| `backend/src/app/apis/backup/preview_backup/sql/q300_reference_axis_option.sql` | `5c3620522bf248a6110ed627129fcf4958f226b4864d74f538f384bed69b2c57` |
| `backend/src/app/apis/backup/preview_backup/sql/q300_reference_catalog_release.sql` | `7aa1f69952b3a989c73f60eb5cd33203010fb3844fa607add6abeaf80994a447` |
| `backend/src/app/apis/backup/preview_backup/sql/q300_reference_food.sql` | `8205cc440da87cdb976aa23bd80064b74e4e837b9c5bab71f71377862af726f1` |
| `backend/src/app/apis/backup/preview_backup/sql/q300_reference_food_form.sql` | `ad1204b842ea11d5727840da19f826cc6f3fe17c5961590cea020d237fde3ae2` |
| `backend/src/app/apis/backup/preview_backup/sql/q300_reference_nutrient.sql` | `0af389ce46200bd40171d0e1094856dd50f87ed96e3784c36f9cd383a7496dfb` |
| `backend/src/app/apis/backup/preview_backup/sql/q300_reference_operation.sql` | `5f6a0d5ee9343b66bcf51f99482cba62f54230600bc97d0ee86516c3a1ed2f31` |
| `backend/src/app/apis/backup/preview_backup/sql/q300_reference_product.sql` | `917dc766b9143fc2fa8aed141f9e45832022f895b8496a7ccbb9cbd51fc3ca7e` |
| `backend/src/app/apis/backup/preview_backup/sql/q300_reference_product_version.sql` | `ebdcf039be11f2e29dd8951a32c9e8d8d676f4acfa577320489bd8e2de0ff956` |
| `backend/src/app/apis/backup/preview_backup/sql/q300_reference_recipe_ingredient.sql` | `ea26158b889928f33f41d304e7668768b2c82535349b0f5626dbc74436657c5a` |
| `backend/src/app/apis/backup/preview_backup/sql/q300_reference_recipe_step.sql` | `c5ab20c6d493a8889f1b5a0b975753efe535aa1f2bdab2f39a4c0ec6b72e1bd4` |
| `backend/src/app/apis/backup/preview_backup/sql/q300_reference_recipe_version.sql` | `1bc6d936ecf91d411d50749451bc016c78e4a95d672f2d3609b7801a7eb44a73` |
| `backend/src/app/apis/backup/preview_backup/sql/q300_reference_resource_type.sql` | `17c2deb1cdfecd510e7d9e4e0ba9c83bcda1338b29256e319767b6e18c6ae445` |
| `backend/src/app/apis/backup/preview_backup/sql/q300_reference_source_record.sql` | `17a5f3941f09d29c395a4ef0d279e89e51e76844221eb5af79692e7ab1b9e7a7` |
| `backend/src/app/apis/backup/preview_backup/sql/q300_reference_unit.sql` | `8caa1a6fed36239bd2d7bd22672cd255fcd9d328393ff0d567b413d8b4d523c3` |
| `backend/src/app/apis/backup/preview_backup/sql/q800_constraints_immediate.sql` | `7c03c4ffbec4374e7c2b6fb317040181c3e3b08eea057b86940d70102fa34ade` |
| `backend/src/app/apis/backup/preview_backup/sql/q801_constraints_deferred.sql` | `92e4ce672420ff25733c0c7fa902dedb804a5b5353abc712d8fd96dba4b5a478` |
| `backend/src/app/apis/backup/preview_backup/sql/q802_restore_profile.sql` | `b0e15aa8ed17d26d29be7eae1a11d6f8d5b5e0750e075697605b72e3a90910a9` |
| `backend/src/app/apis/backup/restore_backup/sql/q001_lock_revision.sql` | `28c2f7fec63fdc8a39f44e0e25d68b8eaa0e0ddb7d99a918e04af3234143ef0e` |
| `backend/src/app/apis/backup/restore_backup/sql/q002_profile.sql` | `49f6e17337f7645e036792de082a441de70b9cba6ef89f80229e5f4e72852ad5` |
| `backend/src/app/apis/backup/restore_backup/sql/q010_export_tables.sql` | `703a6c33c9a8598c3c37c5b39cf22ff286c28ca50b82dac89c9a7571d0ae89a4` |
| `backend/src/app/apis/backup/restore_backup/sql/q020_artifact.sql` | `b9c8654dc89a48abfcefb7739c1e61d0ba399e82ff618c4f89cc25ea62716066` |
| `backend/src/app/apis/backup/restore_backup/sql/q023_lock_intent.sql` | `4e2f2bfb2fc095626d1c50bd7de2f7be5cb8ec3ed0a3bfe059b4703b961ea126` |
| `backend/src/app/apis/backup/restore_backup/sql/q024_consume_intent.sql` | `a82460c8ee631fd6c036207fd13263c4159995cf6dd7501b48a99dc23ccad882` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_catalog_release.sql` | `788fe9694659105cd7b588769f5a8ba6862f5de0604b10721f10d87025f4c336` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_conversion.sql` | `2516b98959e3210c4d77616794b738b423001e4864f647c5345c140efce370d2` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_cooking_session.sql` | `e4c418e253845c782b4eb5772c94ba4fd3a3d9a7be76f2059bb696398f1ab633` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_food.sql` | `e9a343d27f6b16090d78cffc070593b32a6917b7fb7132d9b4858ca02d4fa10b` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_food_alias.sql` | `76f6f6044cdef4be3eb8ba91cc956f3346e7f987a820c59bee74621bc58aa3b0` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_food_allergen.sql` | `202d65291f9a1e9fa01eceb8de32e47ea448463545f296d385aca5b17b5ead4f` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_food_axis_option.sql` | `006d271d9c423fdd0c37edd6ecdbd8c97b15e8cfe46c66c95663e0869c6f016a` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_food_form.sql` | `f04b7465cf8ebbac28e7b706445178dc284933b2758661630fd05e72c71e8170` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_form_yield.sql` | `af108757889088ab842e5054118836464d81dd5da5c1f6d7b804d88bf9930e78` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_ingredient_total.sql` | `7363d86e7820182d4b7f3ea6a572a8faed8c291db93a6dc605ee6d0374ea3aed` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_kitchen_resource.sql` | `ac62a77fe15bc324ba70014344bd3d8a5195f1663f08d7239cd034958a3f0a63` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_menu.sql` | `60d9ff3ddf5d79ff32375683030a8b6250c86b48b75eab96553fe830a039ae77` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_menu_ingredient_override.sql` | `be4cc85b407ed4a6af2865a3d8f485407568f28578949bd39902ca63889a0c33` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_menu_item.sql` | `9b5e1b93cbed61140e86c5d3a04c9a26bdb66a3f1b7c2d14040abcfaf8ae224a` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_nutrition_fact.sql` | `87ca137f255f586bd1ce4b1d1177a4165d44d8f02b0157c5dfbaa82b2117182c` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_pantry_consumption.sql` | `ebeb195f39ba31e57b9467248210e05bc188f48880e7d06e5a59de6b4e60e6df` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_pantry_lot.sql` | `f921c2830d9357c08133f2a9ae03e3e766e165e004512a99478afc758976ef33` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_product.sql` | `2e865c898fef1379cb0fc82c3b637ba957a6322bcccb42b049eb3886514ea801` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_product_allergen.sql` | `ba2b3415f02205c1f51a19d98a1cbff187c4dfb3f35577cf57548fe0767e0367` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_product_component.sql` | `2f916276269a6ee05f44926ea784267836abc1f1575e583082f1f1dad6faea9e` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_product_preparation_rule.sql` | `078fdb27cc7cdf3e19b7a716076b59dcfe1d080aba0f01cf0b7cdb0ae132cdfd` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_product_version.sql` | `6cfc27ac259e1c0d0e74ef7fc69248c4b41d746225789f43c56f8d916875f046` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_receipt_import.sql` | `c848381ee7747c602bd757c29d3e4f12f0e2eca70adf8d405f031cbf92d74717` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_receipt_line.sql` | `3bc87b431b8a29e2c586a2f44afa7d1b2828c6c711bc9c43619c47b5529dd586` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_resource_reservation.sql` | `4640a373130076eaa621ce59b410b01730c13575c0e1031d8820b36bd0d2910f` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_session_task.sql` | `851e7575e5b72a1b45a014e9812f6eaa5a5ef1e96a5cdafc3367223e0c9f804b` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_shopping_item.sql` | `56d08128e320d50c9aadffe0b74734f67068a14e38b37aa00693781b4db0cc62` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_task_dependency.sql` | `8157207df1ff85c0f600177ef8dbb367369b47a1b6d52a02a18e1f9327599175` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_user_exclusion.sql` | `2964224c329b3533669afa23b957c329da4ee069664a999f1efea0065bc1253c` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_user_food.sql` | `921a4cbbf72531bde25180066e67bd7050deafb69ccc55e917168e662c69664a` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_user_pantry_food.sql` | `6278d4a828b1d2b9c9515bdd100336dcdc9738181412871c3045d6a583bdb101` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_user_preference.sql` | `17b30d4baa5717188a88947d0a280186f9ad9da1a52ebf601fc74f098e041beb` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_user_recipe_event.sql` | `70e16a4f267c48b48c2edc74326d982827e307aba1e1a3876dbc7ad8bdb9831e` |
| `backend/src/app/apis/backup/restore_backup/sql/q100_delete_user_shopping_check.sql` | `b6e692637d7bfa0d1bfa9f0d195a6783e01b67583eaf1c0a116d5b94ac0e6ea2` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_catalog_release.sql` | `1f5222a09e4a70b71a23b52c188a945e254db08e50c417de076c8a4bcd8cdfe1` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_conversion.sql` | `cc7e8e2dc6b4dccbdccde79df89ea34c4434a0c77d482155086a3a9445b29224` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_cooking_session.sql` | `7259c2c2e35b584f332510c5e5ba01dd637f349154bd064b20c8872b0150b9a1` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_food.sql` | `ad70bf20fe116835c5fc9969893156918077695a618a0b69e2ed9fba5656e2dc` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_food_alias.sql` | `55a379b5eb0b50d277c1c4c79c2f3aaf7b34ca8f913e4ff82663125ee38c1b3d` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_food_allergen.sql` | `14f3b992c02eced61448184d7ae6bbb669101137264c7cc1b9b0e8ef59b03a1a` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_food_axis_option.sql` | `a24e3bb094def0d08b21aa15e7d2bc71394b01b69ab07b768aba0714c6a08a3a` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_food_form.sql` | `e5a35d8dc2d7e28f80ccf56043b671d79f700d3176b6e1ef316ebca1183932a1` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_form_yield.sql` | `dd79fdde086814b1b2f7e4c6b63b71dca95f0454200be41aceba7f33881bb4e6` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_ingredient_total.sql` | `70780a34840e7dbc4e6afc9027ab53853b36bee1202ebb5e9e9a7f9c3e6e320a` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_kitchen_resource.sql` | `971bce45db5ac8434c49945e86a9d5b8e3075650f8be49316c8f555f7231b22e` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_menu.sql` | `02ed6d8da195820324e78100c93a4d3a6f9b8eb897454c78f2640cf99d570e9e` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_menu_ingredient_override.sql` | `9929e63497ce75ba24b99fbcb80ad91d757a64ff558a98da4eb3e2d04ce75f7a` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_menu_item.sql` | `b6e70b517aaa1232ad887aadb37c3475439e3a9c820353640816851a46de14be` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_nutrition_fact.sql` | `6398d7736ad91430d3fc169cb2daefe6f5d437382e5e7303f59a07db6a69ba57` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_pantry_consumption.sql` | `016dea80bb179b36f08dce4ab92c94c7108cf5841529820fa7de70e944003aff` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_pantry_lot.sql` | `734629f0d3495d28399e1cc2478e01d000a39462ce262f3cf4e93a0735fd7a31` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_product.sql` | `2a9c4834b712d82c0be6e6a1691d26de88903873442aff4a9eecc79a98feee45` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_product_allergen.sql` | `5e8414ff1cb91fb1c7db95680a1f920839ebf34899635c4e13190259ecb245ef` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_product_component.sql` | `5ea2333d0e787a8106b6b2b73835659e3ef6702eeb16d780c8f3b6b758cf33c0` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_product_preparation_rule.sql` | `d6f4516420ae7edd3ca867bcaf69b6b291d0b3835a654cf4a36b67694efa3afb` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_product_version.sql` | `f00ce29801482be5cde208a41ae0cb11e84d26e98da73514c26d14e918007823` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_receipt_import.sql` | `d4c8776ffc8a32fe0a45d1bcbfb86f1be69c4ce90f6208731e842c2ee1afd694` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_receipt_line.sql` | `38b5decf1176dc6834e9b184d78d3821da39cd8e9a7f7a9267315f736641994d` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_resource_reservation.sql` | `cb98c239c7b3a3a4489edd1cc187123f1fb331ac7156905a33b291c07586d823` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_session_task.sql` | `4e2e98a536c6b1959811ecbd84ab08125f90567355826ad1ea275e508c19ea2f` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_shopping_item.sql` | `9a3ce297734d5c68e7fa233916faaf3d14b2ce6f8b5bc609404eedd3dc25ff25` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_task_dependency.sql` | `b43accae305854ac7f73e98129b91f6d9eda58aac7027734b27df2e8eca2ce2e` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_user_exclusion.sql` | `10cd7434d6262ef711c0019f6a13f6b02e944d0de5d04bbe4455ebfd1bc2a7cc` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_user_food.sql` | `413e056710325779644f9b82157b7b360fef45939c93d075f6049c41645d9d1f` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_user_pantry_food.sql` | `d476da8f6d450e9cf156870017d5bc1cc2b8c8a8db9f5317d24a5e1a82e9affc` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_user_preference.sql` | `f59939725d1999d158c70fbf795e141e8a8528721e59540005913f491947f824` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_user_recipe_event.sql` | `cbabe82ebbd9099e5410e4f5e8df98f33df6b87703e1be2e55dccd0bfa524d9c` |
| `backend/src/app/apis/backup/restore_backup/sql/q200_insert_user_shopping_check.sql` | `bfa815ee6e75d46f3b0754fa7edf178538337f3ebc54bd88633879926d29a680` |
| `backend/src/app/apis/backup/restore_backup/sql/q300_reference_allergen.sql` | `0ea865de5e1030261ae49250e80e5b491133d6f6974797254e31d22969e03f06` |
| `backend/src/app/apis/backup/restore_backup/sql/q300_reference_axis_option.sql` | `5c3620522bf248a6110ed627129fcf4958f226b4864d74f538f384bed69b2c57` |
| `backend/src/app/apis/backup/restore_backup/sql/q300_reference_catalog_release.sql` | `7aa1f69952b3a989c73f60eb5cd33203010fb3844fa607add6abeaf80994a447` |
| `backend/src/app/apis/backup/restore_backup/sql/q300_reference_food.sql` | `8205cc440da87cdb976aa23bd80064b74e4e837b9c5bab71f71377862af726f1` |
| `backend/src/app/apis/backup/restore_backup/sql/q300_reference_food_form.sql` | `ad1204b842ea11d5727840da19f826cc6f3fe17c5961590cea020d237fde3ae2` |
| `backend/src/app/apis/backup/restore_backup/sql/q300_reference_nutrient.sql` | `0af389ce46200bd40171d0e1094856dd50f87ed96e3784c36f9cd383a7496dfb` |
| `backend/src/app/apis/backup/restore_backup/sql/q300_reference_operation.sql` | `5f6a0d5ee9343b66bcf51f99482cba62f54230600bc97d0ee86516c3a1ed2f31` |
| `backend/src/app/apis/backup/restore_backup/sql/q300_reference_product.sql` | `917dc766b9143fc2fa8aed141f9e45832022f895b8496a7ccbb9cbd51fc3ca7e` |
| `backend/src/app/apis/backup/restore_backup/sql/q300_reference_product_version.sql` | `ebdcf039be11f2e29dd8951a32c9e8d8d676f4acfa577320489bd8e2de0ff956` |
| `backend/src/app/apis/backup/restore_backup/sql/q300_reference_recipe_ingredient.sql` | `ea26158b889928f33f41d304e7668768b2c82535349b0f5626dbc74436657c5a` |
| `backend/src/app/apis/backup/restore_backup/sql/q300_reference_recipe_step.sql` | `c5ab20c6d493a8889f1b5a0b975753efe535aa1f2bdab2f39a4c0ec6b72e1bd4` |
| `backend/src/app/apis/backup/restore_backup/sql/q300_reference_recipe_version.sql` | `1bc6d936ecf91d411d50749451bc016c78e4a95d672f2d3609b7801a7eb44a73` |
| `backend/src/app/apis/backup/restore_backup/sql/q300_reference_resource_type.sql` | `17c2deb1cdfecd510e7d9e4e0ba9c83bcda1338b29256e319767b6e18c6ae445` |
| `backend/src/app/apis/backup/restore_backup/sql/q300_reference_source_record.sql` | `17a5f3941f09d29c395a4ef0d279e89e51e76844221eb5af79692e7ab1b9e7a7` |
| `backend/src/app/apis/backup/restore_backup/sql/q300_reference_unit.sql` | `8caa1a6fed36239bd2d7bd22672cd255fcd9d328393ff0d567b413d8b4d523c3` |
| `backend/src/app/apis/backup/restore_backup/sql/q800_constraints_immediate.sql` | `7c03c4ffbec4374e7c2b6fb317040181c3e3b08eea057b86940d70102fa34ade` |
| `backend/src/app/apis/backup/restore_backup/sql/q801_constraints_deferred.sql` | `92e4ce672420ff25733c0c7fa902dedb804a5b5353abc712d8fd96dba4b5a478` |
| `backend/src/app/apis/backup/restore_backup/sql/q802_restore_profile.sql` | `b0e15aa8ed17d26d29be7eae1a11d6f8d5b5e0750e075697605b72e3a90910a9` |
| `backend/src/app/apis/backup/restore_backup/sql/q901_advance_revision.sql` | `5f267cc7121b5045dcf1579940e66fc94765ea6bcb57422efc6c6e390c360962` |
| `backend/src/app/apis/backup/restore_backup/sql/q902_append_audit.sql` | `e585649a91c22f7a5f9004996ebce89f3c27b4f55be635e6bd022f1013c5dcf4` |
| `backend/src/app/apis/backup/restore_backup/sql/q903_append_outbox.sql` | `f36d4334935d2601817088aadec9cd24c73302016072ee5f99afe6934952b1e9` |
| `backend/src/app/apis/entities/allergen_create/sql/001_create.sql` | `9be89c330b838df864aff99560f4810a2979b5ebcf2c150b8526592e4188d26c` |
| `backend/src/app/apis/entities/allergen_get/sql/001_get.sql` | `13ab79f5ec0b92f38a56c24f9a8b45f6503605671408b27bdddfc32cc2f9949c` |
| `backend/src/app/apis/entities/allergen_list/sql/001_list.sql` | `c025c7c212cc6d99b68d840cf0f56f0a1e0e5a073e0a124c328f9f78273488c3` |
| `backend/src/app/apis/entities/allergen_update/sql/001_update.sql` | `2c3b57fbbd3e71689791b10292effbb9356f407bcfcaf5e57bb2b38df539fe78` |
| `backend/src/app/apis/entities/app_user_get/sql/001_get.sql` | `8f63dfeb859e9c360a4b45660af3af65ba7eb07d98e1144b863298049e753426` |
| `backend/src/app/apis/entities/app_user_list/sql/001_list.sql` | `d5ed74a9c7e187eccf40653cd71f3e942a333a64b61d3b3e228738ccc6e79217` |
| `backend/src/app/apis/entities/app_user_update/sql/001_update.sql` | `8843682b9f45b72319600d5110ea5f8777cf990a39d46de61c12aa8f886f50d3` |
| `backend/src/app/apis/entities/audit_event_get/sql/001_get.sql` | `2de9783d2ed958a40476843a9734b9bc0059486ff8aada3126970922ee2bf6be` |
| `backend/src/app/apis/entities/audit_event_list/sql/001_list.sql` | `36186f3172bc4bd488def008a8c6ac3c3556f53e9ea902db55e882c10dbf833f` |
| `backend/src/app/apis/entities/axis_create/sql/001_create.sql` | `c389b651eb573b201ae3189865c6df39387f828dfe0a24c5fb8735c105384496` |
| `backend/src/app/apis/entities/axis_get/sql/001_get.sql` | `7602e7378ed88e6889c835cbbd17e9d99a1b974aa3fedd2a764265d7ac696371` |
| `backend/src/app/apis/entities/axis_list/sql/001_list.sql` | `6c35503c05a4ddb24e2f8b1e39ebf307795d7354106d7b04caf09d385c49c9d8` |
| `backend/src/app/apis/entities/axis_option_create/sql/001_create.sql` | `c53afe0609e4c0c0a87cf9cd38a564d44bd5d635ebdfbe2fdcd7a154fa5598cd` |
| `backend/src/app/apis/entities/axis_option_get/sql/001_get.sql` | `23c5abbee75a8285a13f059691ba78e6f7f3f0be244458f67705d10d08298a59` |
| `backend/src/app/apis/entities/axis_option_list/sql/001_list.sql` | `bde17af8420b61b743e23b6ba0109e9fb180027180a22c208cf3ada42a99bd9c` |
| `backend/src/app/apis/entities/axis_option_update/sql/001_update.sql` | `704f2a7a510bae4ee384ac38965321b2f365f7e2f2ed463c3f1209b9f6c05f26` |
| `backend/src/app/apis/entities/axis_update/sql/001_update.sql` | `255f1c463de5727dea61003bf6167edd594f1a0499bbbf5e9bf15696fa3332fa` |
| `backend/src/app/apis/entities/backup_artifact_get/sql/001_get.sql` | `cb3aee6959076ccdcd89e05a8a11866bccb7962869bed83132e81c4e4c2a0c68` |
| `backend/src/app/apis/entities/backup_artifact_list/sql/001_list.sql` | `3ce39417bf2fa051b9a8801dd22336c4d7ba802765555771decb5449c2a606ac` |
| `backend/src/app/apis/entities/backup_restore_intent_get/sql/001_get.sql` | `d052dfc311e00e00865df1434ffb2a21519fdb8eb4eb280dc5eb36d94beba5ac` |
| `backend/src/app/apis/entities/backup_restore_intent_list/sql/001_list.sql` | `752221da7f2ff49e6cef9c132fe75ecac3880375254871d02e5039c066922574` |
| `backend/src/app/apis/entities/candidate_attempt_create/sql/001_create.sql` | `daab30be027ded51ae2b511503fed624101fb568fb1edaabe82dd8494bba9cbe` |
| `backend/src/app/apis/entities/candidate_attempt_get/sql/001_get.sql` | `b0e6dfc372cf72cb8d02d5bf1a9af0445edae8ee6d8e1df220123000564fa8ff` |
| `backend/src/app/apis/entities/candidate_attempt_list/sql/001_list.sql` | `b5b56b5aee6c3b4cec548770a3121bc9c73f66999e85b8ff6763b5d8ff3bf708` |
| `backend/src/app/apis/entities/candidate_attempt_update/sql/001_update.sql` | `ee875e3de576462c3935c0651190d5213562c2b2db295862f7b2f08ea5800039` |
| `backend/src/app/apis/entities/catalog_release_create/sql/001_create.sql` | `d9b6a5e8356d1cd53adf4a2d3fdcd93ea713477fba5ddda418d0247b3a4be651` |
| `backend/src/app/apis/entities/catalog_release_create/sql/002_reference_owner_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/catalog_release_get/sql/001_get.sql` | `0ea08bf312e8db037ba5656bf132f350855f389dc43fdca1c2659705b764102c` |
| `backend/src/app/apis/entities/catalog_release_list/sql/001_list.sql` | `e01aaeb62b7e715e602ae18ea1814d2b8d0283799e1fd981a1a8cf2222a6aa9d` |
| `backend/src/app/apis/entities/catalog_release_update/sql/001_update.sql` | `d2e32f0d67596c0e8680df6a10e661e34793a6c4e4ba5cbbf22c78615edc3f12` |
| `backend/src/app/apis/entities/catalog_release_update/sql/002_reference_owner_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/compatibility_rule_create/sql/001_create.sql` | `7d52dded4fc1b6e398f6e2de3dfc4b08783a0d94c6bd95f3abb35f6199664f80` |
| `backend/src/app/apis/entities/compatibility_rule_get/sql/001_get.sql` | `012cd45a04e748f7ba29cd770ce202737cff664cb6061ee165e7acf3f8da4cbe` |
| `backend/src/app/apis/entities/compatibility_rule_list/sql/001_list.sql` | `628e4ad35d32d990f6984f3a099ffd35f23eab99cf399b9f960c4d73e92fccb5` |
| `backend/src/app/apis/entities/conversion_create/sql/001_create.sql` | `872b71318b9d6d0628f7ca4f95091341dc04e91ad4a3f5b798b46c61aa7da3aa` |
| `backend/src/app/apis/entities/conversion_get/sql/001_get.sql` | `8d9e8d20d372b09458a3efc7c45a6af3277a231ba13b4ef71cadf9873181583f` |
| `backend/src/app/apis/entities/conversion_list/sql/001_list.sql` | `8d64fc59b771cd4b7d3ca10755630b5b93dad537c263ee8167035ef95d3b45b5` |
| `backend/src/app/apis/entities/conversion_update/sql/001_update.sql` | `37d7eb0d24565c325bf9febc8d25d31153a80c50ddcaaf8e483aa11cfb02c684` |
| `backend/src/app/apis/entities/cooking_session_create/sql/001_create.sql` | `6fe1c1d232900e9906de68f594e2ce2d09305948b9496f9f1cfadb416e27a338` |
| `backend/src/app/apis/entities/cooking_session_create/sql/002_reference_menu_id.sql` | `38bbe44f2d294600499f68580cb7f75234f03f36f2464ca79701eb91de7435d2` |
| `backend/src/app/apis/entities/cooking_session_delete/sql/001_delete.sql` | `197cd252207676990ca6b3ad70cb49fca5800bec5823bc7082184793e618cde4` |
| `backend/src/app/apis/entities/cooking_session_get/sql/001_get.sql` | `551bb98a7cf1533229acd2d251a6fcb9d2a8f6d865fd82265230ba5f3f31a252` |
| `backend/src/app/apis/entities/cooking_session_list/sql/001_list.sql` | `c2cbc681c97ca2eab0d24c9d19bff9e5f9d0aba4c4f971983b4c92c58a21b9fe` |
| `backend/src/app/apis/entities/cooking_session_update/sql/001_update.sql` | `066fb75e6acc4f3c913acc3e7f705a72912d7bd2b8451294dcdfa927b28544e9` |
| `backend/src/app/apis/entities/cooking_session_update/sql/002_reference_menu_id.sql` | `38bbe44f2d294600499f68580cb7f75234f03f36f2464ca79701eb91de7435d2` |
| `backend/src/app/apis/entities/food_alias_create/sql/001_create.sql` | `e322571f86616f4584d6384641561644d6fa57dd33e48f9f77b23191b89d79c4` |
| `backend/src/app/apis/entities/food_alias_get/sql/001_get.sql` | `c55bf8e5ed28519678e897f048abb536d4702b3a2d736b1839dc28b3040e8237` |
| `backend/src/app/apis/entities/food_alias_list/sql/001_list.sql` | `7cc230708ff444444ec284e0dd4d4fb63bd42971894da4266aa7698d8d17b45e` |
| `backend/src/app/apis/entities/food_alias_update/sql/001_update.sql` | `9d618eab1d40c2860a32df37b1bc03d52620e6d3c78ec26a80686c888c703728` |
| `backend/src/app/apis/entities/food_allergen_create/sql/001_create.sql` | `c4c2a003f3a0a71eb34a56b9c3defc61ed80f18f9e1da288277e0d2396c4c672` |
| `backend/src/app/apis/entities/food_allergen_get/sql/001_get.sql` | `fd0819857a8071b9516acba4c5482e5b002f3a23d5dd1c59459811a12ff5f1fb` |
| `backend/src/app/apis/entities/food_allergen_list/sql/001_list.sql` | `ba451e98fec60006ebed7fb2093a12e332bd271464c5e57b981cea0b22f1ea83` |
| `backend/src/app/apis/entities/food_axis_option_create/sql/001_create.sql` | `554bee34d8401a1691d55a5cc0190679bf9c086954636e1aed4eabb729ca6ec0` |
| `backend/src/app/apis/entities/food_axis_option_get/sql/001_get.sql` | `0c7807c04696280e3432cea667d20b07dd3aefa4f2d07c2d71c255fb8f424e02` |
| `backend/src/app/apis/entities/food_axis_option_list/sql/001_list.sql` | `81202c2a2ccf438faed6121ed3ff0b7defcbb33bbd82e53fa091bb3a443dfad1` |
| `backend/src/app/apis/entities/food_axis_option_update/sql/001_update.sql` | `6a404ca4bfa31f7f2a5a89d4de71b3caa71c80d3649deba2d218e83158052114` |
| `backend/src/app/apis/entities/food_create/sql/001_create.sql` | `7d6f04f2a89e747bbb1a66b6eed074cf3e846d4241191c644332da7974b4d8e7` |
| `backend/src/app/apis/entities/food_create/sql/002_reference_owner_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/food_form_create/sql/001_create.sql` | `2837cd74cb1d51346e4e6fc9473a9c6302a02f853af0aa99a946da83f41856ce` |
| `backend/src/app/apis/entities/food_form_get/sql/001_get.sql` | `04fe1ee0abee20a1e86150f7fa7110373e3383ca4e4bb6e28c44730c9d098c8f` |
| `backend/src/app/apis/entities/food_form_list/sql/001_list.sql` | `da8f0d5181714a72a69ff46fc46fa5a09161e274cf2f7a2de4dd354181474e9e` |
| `backend/src/app/apis/entities/food_form_update/sql/001_update.sql` | `c7a3e3413de6a2f80868bf5c8d4d91845f58c11f03c24ef4647d239b0d645201` |
| `backend/src/app/apis/entities/food_get/sql/001_get.sql` | `b948e48d279947d51fed51cb4d5f2be264702c70d28e552dd9db17c317402562` |
| `backend/src/app/apis/entities/food_identity_create/sql/001_create.sql` | `1ecc2950fb39e67b6ecf4c0f74b862c842ee91048e34372d554545bfb2372863` |
| `backend/src/app/apis/entities/food_identity_get/sql/001_get.sql` | `7af4c98909aef8587d22ddbf3f9d2513a4bfc0327c7b34fbb88e29874e8c4340` |
| `backend/src/app/apis/entities/food_identity_list/sql/001_list.sql` | `f2ff17b33df0454d8a6e14b2dd159339eba5bde3212138c9f02a790badbbdda1` |
| `backend/src/app/apis/entities/food_identity_member_create/sql/001_create.sql` | `ccef07019de3bf544419fe646a8d3e2d9a673b7b39ee512723b891facbd671fa` |
| `backend/src/app/apis/entities/food_identity_member_get/sql/001_get.sql` | `276ed22f60160476a27c961532617788bee2490d5786dda63360a20f923f557c` |
| `backend/src/app/apis/entities/food_identity_member_list/sql/001_list.sql` | `9b5f6d14e450b9a428eed9cf379f4ff94e4f5d12a28bd935a6f84e26488a9f21` |
| `backend/src/app/apis/entities/food_list/sql/001_list.sql` | `c38fae387dfc44314274bef2600b4a13e08bec2bed6ab3df7ffb806446a30c7f` |
| `backend/src/app/apis/entities/food_update/sql/001_update.sql` | `5cf1833d64d55a6e04159b089f7688e78c7c25ff6150774502fdc701391560aa` |
| `backend/src/app/apis/entities/food_update/sql/002_reference_owner_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/form_yield_create/sql/001_create.sql` | `76782f1120f29bc8c826f42939f6822b5b43a3dad4a5984f44a5e60ab5fce645` |
| `backend/src/app/apis/entities/form_yield_get/sql/001_get.sql` | `ff74c5e65c0c948c2bcafdd6d5ac5e3a7ec755a3dbba380e2043ac003a01f8e9` |
| `backend/src/app/apis/entities/form_yield_list/sql/001_list.sql` | `549251e7644be6a75f0906e096676f9009b09140637b99caa00d5ddb16c9dca1` |
| `backend/src/app/apis/entities/generation_choice_create/sql/001_create.sql` | `16135e8a72cd433c512382373048b23bf259ce0539a866b5b055c68d60a57b99` |
| `backend/src/app/apis/entities/generation_choice_get/sql/001_get.sql` | `e08c7fdb4dc54cab6a9a59811916241ddf64712b6a736b2a5afedc9579090144` |
| `backend/src/app/apis/entities/generation_choice_list/sql/001_list.sql` | `7dfb79d13b3109a1feaa3a87e955828660e75e62e2585b03c8af8ad3ec8ff9e4` |
| `backend/src/app/apis/entities/generation_choice_update/sql/001_update.sql` | `53d4628fbc2cbd96d93cc38d99877b155332a8d33bc1a3c15649f5e9003a7bf2` |
| `backend/src/app/apis/entities/generation_food_create/sql/001_create.sql` | `8505f3682f3b465cf0c00f4b1c2a5b9dd2c50c7d19960ed2ba5753fd4fbed059` |
| `backend/src/app/apis/entities/generation_food_get/sql/001_get.sql` | `96d3bc18c8ed300b163e86a8afdc10e7275092e26a8a79909f150fc156a687ca` |
| `backend/src/app/apis/entities/generation_food_list/sql/001_list.sql` | `0b6893ec2e3d35e42131c0960616a5c5ac92265c4af68e1045d312b61624d11a` |
| `backend/src/app/apis/entities/generation_food_update/sql/001_update.sql` | `badcdc60ea8b2c1496b2c108964d8300e8d1d429bf2c7cf8096450755c634283` |
| `backend/src/app/apis/entities/generation_job_create/sql/001_create.sql` | `54bfdb5eccb413e3c3aa05866c3941f28fc9bcdf5190c30b3a8ef42bf38d23fc` |
| `backend/src/app/apis/entities/generation_job_get/sql/001_get.sql` | `56aa0c1e8f94741879f3caf284b4a09b72a99e8f5a316720074eff1e1cc69728` |
| `backend/src/app/apis/entities/generation_job_list/sql/001_list.sql` | `7fe9c65ae6886a44ad41765ba45e1676a97356ffd2a2acdd645952aca17c64e7` |
| `backend/src/app/apis/entities/generation_job_update/sql/001_update.sql` | `adec6bb24298823efcd31339644a1234085726d0d3e8358c737a5580874d7087` |
| `backend/src/app/apis/entities/generation_policy_create/sql/001_create.sql` | `f307ebb9cf1951936044cd84a7e3a6de8cc366ce8e9ff9661cae1010af0ce3be` |
| `backend/src/app/apis/entities/generation_policy_get/sql/001_get.sql` | `634b7b06efa3702b7ab7ac2952f0a3f4ad31a0e8538fffd34229a3e65a6281ba` |
| `backend/src/app/apis/entities/generation_policy_list/sql/001_list.sql` | `f4edbc347431cd2fa4f84100187e4ce44e43b3aa94dc624325fc7b9beb5c921b` |
| `backend/src/app/apis/entities/generation_result_create/sql/001_create.sql` | `c5015478d5550affa35028a96025082f35d580d0b34e21481ad1fc689b0ce58d` |
| `backend/src/app/apis/entities/generation_result_get/sql/001_get.sql` | `42c5d92356b4a7e662dd21a49ae2a2cb2761e3dcc0f0adb72d3691708ee85f7f` |
| `backend/src/app/apis/entities/generation_result_list/sql/001_list.sql` | `94209fa77a9e0e69f75cd68b331e305cf17c6549f6f292d433dbd45b377c0ef8` |
| `backend/src/app/apis/entities/generation_shard_create/sql/001_create.sql` | `486a1399fe402bdbc246977fa73dbf903b23be209ea8724e2d18326dc1cc3a25` |
| `backend/src/app/apis/entities/generation_shard_get/sql/001_get.sql` | `c7e931fd4758c5e28f0432a981287ff53693278bb0ce736b589ccd7fb525aa62` |
| `backend/src/app/apis/entities/generation_shard_list/sql/001_list.sql` | `d983e42c109b45b6185f0f3ec537d54d405a72f7aa0c7f38bf0b4bc3910c0a8c` |
| `backend/src/app/apis/entities/generation_stratum_metric_create/sql/001_create.sql` | `2f84f17f7dbed7e9922a41f495cd12535f7023b3c6e26a7eadede708bf186c05` |
| `backend/src/app/apis/entities/generation_stratum_metric_get/sql/001_get.sql` | `302298afc1a5585f872ea7755968343f0d73e1771683546d64e3fd9c25d1d29c` |
| `backend/src/app/apis/entities/generation_stratum_metric_list/sql/001_list.sql` | `fba1a697b762e9be1bc9c1e544a7554eb2b053d0c948710b594cf395e65102ea` |
| `backend/src/app/apis/entities/generation_template_create/sql/001_create.sql` | `18479c8c8a5f15761ce19175131882b4daf99386ba1520f993a4441d7ea9d7e9` |
| `backend/src/app/apis/entities/generation_template_get/sql/001_get.sql` | `aef179abafc1d879f0bba35f10cb300ae7607b0910700b2e7c84b3440856dcbc` |
| `backend/src/app/apis/entities/generation_template_list/sql/001_list.sql` | `4bc8927ac1a783c58e3cc0d44401895ed17c2b5db300e2ba65238f929d6def60` |
| `backend/src/app/apis/entities/ingredient_total_get/sql/001_get.sql` | `86af6c2bccc1f4e95b6107b6bde7d3064859dae2cac1c45576cc70159666af80` |
| `backend/src/app/apis/entities/ingredient_total_list/sql/001_list.sql` | `cad7d3d1065f0443fd574c008258e396a358ee550e520849b8666a203ae0ac10` |
| `backend/src/app/apis/entities/kitchen_resource_create/sql/001_create.sql` | `6f8e0e1786131646a7302073fa43a52287c24748dbafc9249743ba985e26355b` |
| `backend/src/app/apis/entities/kitchen_resource_create/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/kitchen_resource_delete/sql/001_delete.sql` | `beda7f45537f3112fe610c5bf26b5d732789abe1ac34e3b3c6360aa25542ebc5` |
| `backend/src/app/apis/entities/kitchen_resource_get/sql/001_get.sql` | `0b12862b268e6fc7f1296c1d5e523cc6fd774c65fbccaa46c053bdf512db11f6` |
| `backend/src/app/apis/entities/kitchen_resource_list/sql/001_list.sql` | `d5750111b150bdc8cf69ad24862774b3a1c5b0c479691ee3014bcd07c0aeac59` |
| `backend/src/app/apis/entities/kitchen_resource_update/sql/001_update.sql` | `bde2062b9708e41dd74bd4fca0286a9ac3ab6e8a38bc168728f667a8156d0f14` |
| `backend/src/app/apis/entities/kitchen_resource_update/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/material_node_create/sql/001_create.sql` | `b43c5c29e27ed42362eff92f94178fa3dd1373364038599b4b121ac7b8d14d83` |
| `backend/src/app/apis/entities/material_node_get/sql/001_get.sql` | `583f3e746355c693561105f301215c7982438ccd443c3055c6d5b199744e6148` |
| `backend/src/app/apis/entities/material_node_list/sql/001_list.sql` | `65c4ea21200c82a55349c04887d1780ba37c35a3cf6cad1e62a4284c3b68410a` |
| `backend/src/app/apis/entities/material_node_update/sql/001_update.sql` | `8fcb43a764e28bf0ce414ecc1c1f86abe43bfda1c528d497e6424e19539739c0` |
| `backend/src/app/apis/entities/media_asset_create/sql/001_create.sql` | `dc36b723a78bef40ebf1a2c03e90983a8f8f31c718af845d1b38badceecb5897` |
| `backend/src/app/apis/entities/media_asset_get/sql/001_get.sql` | `84240baa1fa87403c5a91ed488e16e085b766dccd4491df74aa456fb3ce8fe30` |
| `backend/src/app/apis/entities/media_asset_list/sql/001_list.sql` | `44d85b2fdfc83b9cf546dd692e0670847c805841a6c07a70d659e684f9f29ba3` |
| `backend/src/app/apis/entities/menu_create/sql/001_create.sql` | `c3280b43af90661ee94c04b0a1371ebd2bb11968d664d4c399ed35dc4f6da6d2` |
| `backend/src/app/apis/entities/menu_create/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/menu_delete/sql/001_delete.sql` | `c54bb953a1aec2d46447721d3d40561f4c16397ff475763302568daf648f0e99` |
| `backend/src/app/apis/entities/menu_get/sql/001_get.sql` | `9b80ca204516a5eee8da44a5766e773f6a005d9abab839e3ddd31d255ba891ef` |
| `backend/src/app/apis/entities/menu_ingredient_override_create/sql/001_create.sql` | `93c25eb344c0a36744ee723de536b2fe3eab4d404a9190f50baecbb423b74c17` |
| `backend/src/app/apis/entities/menu_ingredient_override_create/sql/002_reference_menu_item_id.sql` | `42657c3b816bba623f330c373d35b2480ebafbb4a16ec449a0c244269aa8d465` |
| `backend/src/app/apis/entities/menu_ingredient_override_delete/sql/001_delete.sql` | `c2f78817c7ed55f0f04b08f248660a871e528eeefdf15b17ed0d2dd198989971` |
| `backend/src/app/apis/entities/menu_ingredient_override_get/sql/001_get.sql` | `a8d194b989c108cc4d27b0127365b16d2c2a5c7c076a96c40075643a03473098` |
| `backend/src/app/apis/entities/menu_ingredient_override_list/sql/001_list.sql` | `4fe54ed6dd5538eb79c1c2fd674f3a508884de1d714eb50b6fbf67bdc920f961` |
| `backend/src/app/apis/entities/menu_ingredient_override_update/sql/001_update.sql` | `ce3eb586e20e4f4e3e2dae2b11bac861199b685af91a2002563a6f74fb2d1c7f` |
| `backend/src/app/apis/entities/menu_ingredient_override_update/sql/002_reference_menu_item_id.sql` | `42657c3b816bba623f330c373d35b2480ebafbb4a16ec449a0c244269aa8d465` |
| `backend/src/app/apis/entities/menu_item_create/sql/001_create.sql` | `d7e1246fc7cef12156481c520e150dd2b12723c8ba13ee661619100edc474d90` |
| `backend/src/app/apis/entities/menu_item_create/sql/002_reference_menu_id.sql` | `38bbe44f2d294600499f68580cb7f75234f03f36f2464ca79701eb91de7435d2` |
| `backend/src/app/apis/entities/menu_item_create/sql/003_reference_recipe_version_id.sql` | `ecd6085d7f005353af0c3ccda7e5e73170f30de1385d9ce845a310599d23d8fa` |
| `backend/src/app/apis/entities/menu_item_delete/sql/001_delete.sql` | `875e7601257f85f4c2bf27b359bb9967b34539b4ffbde3698e76ac278735ca7c` |
| `backend/src/app/apis/entities/menu_item_get/sql/001_get.sql` | `3bd544eab0e069f8f8c5578243b3d338e473eec5e72861a51fb7535cd7bcdcae` |
| `backend/src/app/apis/entities/menu_item_list/sql/001_list.sql` | `6c189ebc35407f7ca5d6acd016b302b0c2c220356951c34dc1d6eca1f3eb2520` |
| `backend/src/app/apis/entities/menu_item_update/sql/001_update.sql` | `17fc8d31a6b713916b1faf79553da981de3b3bb6fda8a979247c64631c839731` |
| `backend/src/app/apis/entities/menu_item_update/sql/002_reference_menu_id.sql` | `38bbe44f2d294600499f68580cb7f75234f03f36f2464ca79701eb91de7435d2` |
| `backend/src/app/apis/entities/menu_item_update/sql/003_reference_recipe_version_id.sql` | `ecd6085d7f005353af0c3ccda7e5e73170f30de1385d9ce845a310599d23d8fa` |
| `backend/src/app/apis/entities/menu_list/sql/001_list.sql` | `aafae8ccf19dca2c35659f54aa5ae437b285ffcfdcdeadc66cac463ccab885b5` |
| `backend/src/app/apis/entities/menu_update/sql/001_update.sql` | `08d43b254aa3adddee761db5c2c4aa6a2c30640cb789f3ffadd934fca2f71180` |
| `backend/src/app/apis/entities/menu_update/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/nutrient_create/sql/001_create.sql` | `71b2938fcc718c41098a53acb1b04f0f7c59adae14f8b02edec07c1d4c4c1a5f` |
| `backend/src/app/apis/entities/nutrient_get/sql/001_get.sql` | `12319d2c885e20e5663c4fadcf8311f090e525d074556225f6fcf2e3e820c5ae` |
| `backend/src/app/apis/entities/nutrient_list/sql/001_list.sql` | `670cb0837a64bf47ceb87f638c813411b2855974814d1a031c27ce36e78c7279` |
| `backend/src/app/apis/entities/nutrient_update/sql/001_update.sql` | `49ec854ea28394cd51e1aa79d6e23d0671f62739ddb2120b68ad1c7440ca1254` |
| `backend/src/app/apis/entities/nutrition_fact_create/sql/001_create.sql` | `0f30dbcfabdb284f2c625eeccc016cf6d1c5ec1da6002e95bc6fd798a6e4b441` |
| `backend/src/app/apis/entities/nutrition_fact_get/sql/001_get.sql` | `cf72745dace31a8f09454369c066d502247d7b6f169d8662f0a2bfdafa916724` |
| `backend/src/app/apis/entities/nutrition_fact_list/sql/001_list.sql` | `001fe9bba2c53d40dda38a6200b0cefb1cb8737d4970dc83e21c94515a4a25c0` |
| `backend/src/app/apis/entities/operation_create/sql/001_create.sql` | `c00688e45b7f43ebd39359f6ec4e6cdd2dd9df81fdef8ae3d0d7b152800f4c12` |
| `backend/src/app/apis/entities/operation_get/sql/001_get.sql` | `875c2f488765dfe82823de0e253f95932ce9f6400f68900f54b31734d6e35c7e` |
| `backend/src/app/apis/entities/operation_list/sql/001_list.sql` | `8d0fd4d3c2ec52c57f8947a5e4a8e35cb62e3f606b6822e0633c444b1f57c499` |
| `backend/src/app/apis/entities/operation_parameter_create/sql/001_create.sql` | `2b52340fefd46b99f43910cc33bee8a1be677c58c6ea4457e8b1e651769d9395` |
| `backend/src/app/apis/entities/operation_parameter_get/sql/001_get.sql` | `c95e474cea9e8c5be9d5c74126db5e89d3ab27f4881a5a144804af99ea51d1d9` |
| `backend/src/app/apis/entities/operation_parameter_list/sql/001_list.sql` | `9279840a42bda971ee001437a37fa68bb5a79a1f2356da1ee9f4bb0821a74f9e` |
| `backend/src/app/apis/entities/operation_parameter_update/sql/001_update.sql` | `2e891193d90cb55d6852384e6b5d003068ed269b37da4fcafc2eaee0d60b401d` |
| `backend/src/app/apis/entities/operation_update/sql/001_update.sql` | `b3789d6710bb2d628c15663b0f96ac217c58912e7d9f823c4f6a05c01c62cafd` |
| `backend/src/app/apis/entities/outbox_event_get/sql/001_get.sql` | `65e0fddd65666b36000a4428d254b73c08829736de5a5e67ae963ba8f197c661` |
| `backend/src/app/apis/entities/outbox_event_list/sql/001_list.sql` | `9c72edd45eb1790e92bcac03c873d578ceeb1cca5c0e8fbfb265f3671a653b05` |
| `backend/src/app/apis/entities/pantry_consumption_get/sql/001_get.sql` | `cfa72d1d0fcfe19b48ce59f59b8dd56352802d53c7c48e1d25e5cd4ea8ada797` |
| `backend/src/app/apis/entities/pantry_consumption_list/sql/001_list.sql` | `0054553cc363c5e3833a78d470bd102068e240f0f2fcd672688ef896f66ca4a4` |
| `backend/src/app/apis/entities/pantry_lot_create/sql/001_create.sql` | `b69051728d8046f8f7ecac85ec850a2e4c06bd3ee248ed1a000673858355794b` |
| `backend/src/app/apis/entities/pantry_lot_create/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/pantry_lot_create/sql/003_reference_source_import_id.sql` | `a77f11932f5cd68fbe08752aeec565298584e2f6f42b91d06502489fc622d64e` |
| `backend/src/app/apis/entities/pantry_lot_delete/sql/001_delete.sql` | `8505e722668bd264503964882a10f1fbc3470506c8b3ada6eb0440dcae16bf5e` |
| `backend/src/app/apis/entities/pantry_lot_get/sql/001_get.sql` | `ef61d970e7c120dade3f7dfedfce57d7c74d258601203aca9a2e659fbf8b3c17` |
| `backend/src/app/apis/entities/pantry_lot_list/sql/001_list.sql` | `a0ede6c1fbec6a236a27448357d3f680d1e5ebf7e6414ffa4a8c553dd7ded3a0` |
| `backend/src/app/apis/entities/pantry_lot_update/sql/001_update.sql` | `dbdbaa0e8169930e6da51bde67ceb5d327120afbb0fbcbd127eb036f059a6767` |
| `backend/src/app/apis/entities/pantry_lot_update/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/pantry_lot_update/sql/003_reference_source_import_id.sql` | `a77f11932f5cd68fbe08752aeec565298584e2f6f42b91d06502489fc622d64e` |
| `backend/src/app/apis/entities/product_allergen_create/sql/001_create.sql` | `ea6a5211a3b3ef2e2bf3ccf573ded109afb0d5d91feda1ef2a4765edbcddd00a` |
| `backend/src/app/apis/entities/product_allergen_get/sql/001_get.sql` | `fbc5bd7b3dabf55598d1c28c353b958860700ce7e3acc27c6092f0b5b67dd8d5` |
| `backend/src/app/apis/entities/product_allergen_list/sql/001_list.sql` | `29280f8ac99fe8e4b4c1dcd1ac865bdd0773fd0b8770f0f90eb139d08b9d7e3f` |
| `backend/src/app/apis/entities/product_component_create/sql/001_create.sql` | `1ac5228e7b5e10081706e5780d86b434f0912359c92a4f9bb42f0a9fc1aaa44f` |
| `backend/src/app/apis/entities/product_component_get/sql/001_get.sql` | `f87fc50518b558677c3f057581865d8fba0fb402bdc8278f1bdbd6c849b4e018` |
| `backend/src/app/apis/entities/product_component_list/sql/001_list.sql` | `9eb4b389e521dbf7b3d7caf9580749999819682dff1bb3da7f453b6a2006320c` |
| `backend/src/app/apis/entities/product_create/sql/001_create.sql` | `fd3c40039513e2bbe3a5cf02d22129a6f8bc47f9b0f20b87d7aa28110ed0c2ea` |
| `backend/src/app/apis/entities/product_get/sql/001_get.sql` | `8cbc20c958fb66ecfc318a5bf3782f88dc400605e6183d50291471f55b6b12aa` |
| `backend/src/app/apis/entities/product_list/sql/001_list.sql` | `1fdaa0473cb542b645d9f3fd024207076add0e4ba15f5bc573b60e8af0f188db` |
| `backend/src/app/apis/entities/product_preparation_rule_create/sql/001_create.sql` | `aed779c9085318e3b111674b71a8bd41d0af60aa5b7108f0e28214f7f7e238c0` |
| `backend/src/app/apis/entities/product_preparation_rule_get/sql/001_get.sql` | `5413f3de6361ebe74905efeed8ce4dfbe739a9cecbc0d7aa416de46875b1e830` |
| `backend/src/app/apis/entities/product_preparation_rule_list/sql/001_list.sql` | `ea0866de9c092d674d242a7d9681426ab02a6efe5075abcc256046b6000fd44f` |
| `backend/src/app/apis/entities/product_update/sql/001_update.sql` | `00a80b3c085a379b38fd51be5e842f5beaf158188f422b2b0076fe021f38ee14` |
| `backend/src/app/apis/entities/product_version_create/sql/001_create.sql` | `1aaa7f209516c50f48f839b5420f1873161b9034056e48d09503811ba7af2293` |
| `backend/src/app/apis/entities/product_version_get/sql/001_get.sql` | `316db947889b90cbe1614133b80369ce51dcca4b63d040ac2511d70385e19b8e` |
| `backend/src/app/apis/entities/product_version_list/sql/001_list.sql` | `4582eb2841ca6f9b310e05b7303665ae3d225d966dcf50f20eab8d5b37dc9190` |
| `backend/src/app/apis/entities/receipt_import_create/sql/001_create.sql` | `b5446e9a9d5ecf346556802d6b5eb1b428e02a208889af57a4bd4a98e01ca610` |
| `backend/src/app/apis/entities/receipt_import_create/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/receipt_import_delete/sql/001_delete.sql` | `634fa32a01345932305c4bbf23cda9933687158d2e2cbebf09229d38c751888c` |
| `backend/src/app/apis/entities/receipt_import_get/sql/001_get.sql` | `cdbe65d9c729420f694b5f8d75acd2ab4932975a98503310a274c1a1519d5837` |
| `backend/src/app/apis/entities/receipt_import_list/sql/001_list.sql` | `e8d140055314f088e4b70d8af09b941856a6398a523aa5905c20002316126438` |
| `backend/src/app/apis/entities/receipt_import_update/sql/001_update.sql` | `186013f167807fa9697a59b1513b4c341b63c351bc53c1db08331b37a13bdf97` |
| `backend/src/app/apis/entities/receipt_import_update/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/receipt_line_create/sql/001_create.sql` | `a6e6c3a0327b1af2931e73921d1fb5806a10fdd29305bd805209f98e302b0058` |
| `backend/src/app/apis/entities/receipt_line_create/sql/002_reference_import_id.sql` | `a77f11932f5cd68fbe08752aeec565298584e2f6f42b91d06502489fc622d64e` |
| `backend/src/app/apis/entities/receipt_line_create/sql/003_reference_pantry_lot_id.sql` | `dc07120f21e466f7b2099ea4c991e7fbe1a0d519a1d91d3ed3722ac7adc38de8` |
| `backend/src/app/apis/entities/receipt_line_delete/sql/001_delete.sql` | `13e1622107802407a6ffc0d7a11adcc384843d5cb533d1dddde2c69e44640fe8` |
| `backend/src/app/apis/entities/receipt_line_get/sql/001_get.sql` | `b9a6d8d283ada177316cb03a2bd86fe82e780b13e28b7491c3ae59435df3cb40` |
| `backend/src/app/apis/entities/receipt_line_list/sql/001_list.sql` | `ef3e992a9ec0e4841f576b6a22b2de4e207cc40f211ba132009358b40b9c100c` |
| `backend/src/app/apis/entities/receipt_line_update/sql/001_update.sql` | `9f71906351d2a8fcc7fc77c6ed1e1c7176fbda68478e78077e452e8df4d8217a` |
| `backend/src/app/apis/entities/receipt_line_update/sql/002_reference_import_id.sql` | `a77f11932f5cd68fbe08752aeec565298584e2f6f42b91d06502489fc622d64e` |
| `backend/src/app/apis/entities/receipt_line_update/sql/003_reference_pantry_lot_id.sql` | `dc07120f21e466f7b2099ea4c991e7fbe1a0d519a1d91d3ed3722ac7adc38de8` |
| `backend/src/app/apis/entities/recipe_create/sql/001_create.sql` | `1291059e0023aaa096a815a393d7ee0e91d90e27f4679364d4abb54c0bec0dcd` |
| `backend/src/app/apis/entities/recipe_embedding_create/sql/001_create.sql` | `fc810b40bd890fc6155b797a1605b4ea78432e468e1b5429e11943e0bf43b1a5` |
| `backend/src/app/apis/entities/recipe_embedding_get/sql/001_get.sql` | `c90ad2039e59c2cb52a5c812614ab45835774a7eaa150364f7585cd858dc8a93` |
| `backend/src/app/apis/entities/recipe_embedding_list/sql/001_list.sql` | `6a1ac37a2b3183d4ebe84545bfe1efc1e92eae438f0b75ff5816911068d4453e` |
| `backend/src/app/apis/entities/recipe_embedding_update/sql/001_update.sql` | `78098faf093a02f8f9b953151778d83cc4e8fa2227aaf0ab3f7afcef2e838bf7` |
| `backend/src/app/apis/entities/recipe_get/sql/001_get.sql` | `074b98219fc63b31f6f0fe380dcf158061b2e6e9444e2f4bd8f57842fb3892f4` |
| `backend/src/app/apis/entities/recipe_ingredient_create/sql/001_create.sql` | `ade300e5d49f88ee2e09ccfa80a2b88ceb28448459ae90ca628d41bd019af3d8` |
| `backend/src/app/apis/entities/recipe_ingredient_get/sql/001_get.sql` | `8c7f1e20f4e54b2100965fbf149a905b62469a882d305984a67e945c4dba7d96` |
| `backend/src/app/apis/entities/recipe_ingredient_list/sql/001_list.sql` | `c034d0ca54863ffcedff1e982611f3c82063cd34d67497483b30bdcab34fdc30` |
| `backend/src/app/apis/entities/recipe_ingredient_update/sql/001_update.sql` | `efbc3ddb2f2f9550033d400d803609bc2571fda76e3efebeccb14c4739ab216d` |
| `backend/src/app/apis/entities/recipe_list/sql/001_list.sql` | `85aa67a38b8ca49bb2e76f727de1ca558e6dae78c9529fa41be398220590b630` |
| `backend/src/app/apis/entities/recipe_option_create/sql/001_create.sql` | `dd79a113cf6c90c4811bde2a768104c1944b36f96cf49b9adfe725b75f6f5adf` |
| `backend/src/app/apis/entities/recipe_option_get/sql/001_get.sql` | `78776e345cfd46eb646bf2864951c346c93578373f306a3ae60217c9a6f71b94` |
| `backend/src/app/apis/entities/recipe_option_list/sql/001_list.sql` | `97fdc004758bca73546d8c0a22b1889e994a9a45fa0fbfbd844ed4943f1496c6` |
| `backend/src/app/apis/entities/recipe_option_update/sql/001_update.sql` | `6e4292855ecd73ef9bbd1c96300833df827ccddc789385861a0209bd5f575f5d` |
| `backend/src/app/apis/entities/recipe_search_document_get/sql/001_get.sql` | `29724bb55c7be89f8964fef9c05a2bd4275065093c2806e7552a9ffc227f2d02` |
| `backend/src/app/apis/entities/recipe_search_document_list/sql/001_list.sql` | `93e2882f24e7b1c8bfa19f85a382ce42a46229deaac0c3f13d92ebe4d5f569ab` |
| `backend/src/app/apis/entities/recipe_signature_create/sql/001_create.sql` | `b29a2ec9231170a9d180d8f98295f11c3a794f27e9a5b7438e6bb520d4e943f9` |
| `backend/src/app/apis/entities/recipe_signature_get/sql/001_get.sql` | `6ce309540a1874daeedd6b2b4d1bcd9ce90efe3efb2c41de87738cbc89ea96f8` |
| `backend/src/app/apis/entities/recipe_signature_list/sql/001_list.sql` | `fe82abe744ea4bb7be4723d56ed7ba99638320aedbfc053f117f44606de248e5` |
| `backend/src/app/apis/entities/recipe_similarity_create/sql/001_create.sql` | `82a98adb0b3e937bf0a12b55e6e1524d897dcb6f6f3f2400ba2b9d520132b5d7` |
| `backend/src/app/apis/entities/recipe_similarity_get/sql/001_get.sql` | `f30d688f3edcd4ad4001eb573d36d0de6d36775399bb7bf6774c0ba02fe2f42a` |
| `backend/src/app/apis/entities/recipe_similarity_list/sql/001_list.sql` | `9c9151af745241773a5b662fb8736e24680e08a46ee8322c27a3e0d1b667bad8` |
| `backend/src/app/apis/entities/recipe_similarity_update/sql/001_update.sql` | `7d84dfd682d0954327c3011ffaa727838905ab3d8941e3268d611e4848ebbbac` |
| `backend/src/app/apis/entities/recipe_step_create/sql/001_create.sql` | `910cfc6974da5900ffee6957b59af8e5844555708838845d8c850d42df14fe69` |
| `backend/src/app/apis/entities/recipe_step_get/sql/001_get.sql` | `7b70fa110769347b4c3a30807a4aa3d4d44c1dd3543c44b1418fc96adb0d58b2` |
| `backend/src/app/apis/entities/recipe_step_list/sql/001_list.sql` | `663ba354925f2ae4a0bd9e49e6d9373347436f631ced9284f4e9f717457a864a` |
| `backend/src/app/apis/entities/recipe_step_update/sql/001_update.sql` | `26c88bc6ccd6d23655d283358e7c89bd7b65afda6427a26d360a16c1a49ce3dd` |
| `backend/src/app/apis/entities/recipe_update/sql/001_update.sql` | `0a0fc3d04304aafd5f3ba094e4d3accf37036c6d4bebd34886486712ca302d4b` |
| `backend/src/app/apis/entities/recipe_version_create/sql/001_create.sql` | `a8b1db5065507a831712d11eafb0b8bc171ea55874d56b49ad1e54e6ab864b01` |
| `backend/src/app/apis/entities/recipe_version_get/sql/001_get.sql` | `1f646b445a4f6aa97b423cdda91fa3d9583fcac388a84133537f389278767092` |
| `backend/src/app/apis/entities/recipe_version_list/sql/001_list.sql` | `21a1c7097d74e8a2a99894478dbb9726fd618ec74446b5205855dd3d8be53ff4` |
| `backend/src/app/apis/entities/recipe_version_update/sql/001_update.sql` | `9356277453f1adfb3e7955eca3428c9379585ac41ffcf4e52d41968ced48a95e` |
| `backend/src/app/apis/entities/resource_reservation_create/sql/001_create.sql` | `485bf6c1f5886ee9be208fe5337d783f504eec066747c8db1cb8796a0236f7c9` |
| `backend/src/app/apis/entities/resource_reservation_create/sql/002_reference_task_id.sql` | `b4d2fadb4db4cdb9fa656f5bf72e16c0fca491e6249721ca43bbdecaaa52bd12` |
| `backend/src/app/apis/entities/resource_reservation_create/sql/003_reference_resource_id.sql` | `6c037285033467ba549a0b007ee1fd3c8bcb72b0eb03911b87e2ed0301d23f46` |
| `backend/src/app/apis/entities/resource_reservation_delete/sql/001_delete.sql` | `ca957d5ccbd043142a0de25eeb5fd09e9c270b8bd42beadf88fa43f54f83bc0a` |
| `backend/src/app/apis/entities/resource_reservation_get/sql/001_get.sql` | `1ac71ed3bdd9cdfa2c8ea16fbb215cd5f8f14355fd2789a0afce43d7720de154` |
| `backend/src/app/apis/entities/resource_reservation_list/sql/001_list.sql` | `b4ba27456a184def19ffa780cda3eb094b379fada33030a0e22f88871d7d578b` |
| `backend/src/app/apis/entities/resource_reservation_update/sql/001_update.sql` | `4e25af4c9586233a42a88eeb7c661c5b9dc47f4a70bcb13469ed8164835209df` |
| `backend/src/app/apis/entities/resource_reservation_update/sql/002_reference_task_id.sql` | `b4d2fadb4db4cdb9fa656f5bf72e16c0fca491e6249721ca43bbdecaaa52bd12` |
| `backend/src/app/apis/entities/resource_reservation_update/sql/003_reference_resource_id.sql` | `6c037285033467ba549a0b007ee1fd3c8bcb72b0eb03911b87e2ed0301d23f46` |
| `backend/src/app/apis/entities/resource_type_create/sql/001_create.sql` | `c8fa8be0892be20a59ad447b3dbf8f95481f7e6285a61b423e663f76db5abb5a` |
| `backend/src/app/apis/entities/resource_type_get/sql/001_get.sql` | `29f9d2bb522e920966f41b7956ad92d14065fa2818249779399edf38536de8e6` |
| `backend/src/app/apis/entities/resource_type_list/sql/001_list.sql` | `274946c9b54f6bb3b356fa90421fefa6f293e1f3bccd143880a1ac032d152595` |
| `backend/src/app/apis/entities/resource_type_update/sql/001_update.sql` | `1fa9e9802e05cb015834487ceb1ea6d2aa6d1017cd523420fab2d015767c9b9a` |
| `backend/src/app/apis/entities/scaling_point_create/sql/001_create.sql` | `e1b0e218a5e864120ccfa76f373bcaebd4112ce0a344bd6af9ce9abb0104be67` |
| `backend/src/app/apis/entities/scaling_point_get/sql/001_get.sql` | `70afb231bf8649d702182a3e01943878638e56f6a4811edfec498f4694337fbd` |
| `backend/src/app/apis/entities/scaling_point_list/sql/001_list.sql` | `7c1bce30df9a3a83080cc79fe62aba5319d0b4198a9f396dfeca6f1e54c7ac8b` |
| `backend/src/app/apis/entities/scaling_rule_create/sql/001_create.sql` | `d146f6cf770d0d869fcb7d86366cceb94a4f967d00db38ad48cdad015bf45b95` |
| `backend/src/app/apis/entities/scaling_rule_get/sql/001_get.sql` | `35a24ded5382bba53ddc9d3a2f483bedec35a2446ac3d469a1ecafe79d508c0b` |
| `backend/src/app/apis/entities/scaling_rule_list/sql/001_list.sql` | `31a824f845fa786f6dce6aaecfd76ecba1c8a1a6b644b4b7aa8c55c789958828` |
| `backend/src/app/apis/entities/session_task_create/sql/001_create.sql` | `9a6fac339b236f1881835966047a0640e9cf92d52a66e3bf3b60e2addd6fc84e` |
| `backend/src/app/apis/entities/session_task_create/sql/002_reference_session_id.sql` | `73a5b96119235ec47105b6d918874a63ddb723cf98434dab7e722384f3456467` |
| `backend/src/app/apis/entities/session_task_create/sql/003_reference_menu_item_id.sql` | `42657c3b816bba623f330c373d35b2480ebafbb4a16ec449a0c244269aa8d465` |
| `backend/src/app/apis/entities/session_task_delete/sql/001_delete.sql` | `b13897c5bfd198e38bdc96ee86a2184e2ac60334650be1a9ac0bec37dacda7b5` |
| `backend/src/app/apis/entities/session_task_get/sql/001_get.sql` | `b0205c3c2b8f8c5515bab5b7ccd11c86e74373df9ca6bacae43199eea5a44d67` |
| `backend/src/app/apis/entities/session_task_list/sql/001_list.sql` | `226b7d1074fa82969a5ce2e050981cf134b27d82981c038d578acdc1034129ad` |
| `backend/src/app/apis/entities/session_task_update/sql/001_update.sql` | `2b0680a617d11c258276c0739433fdc7c2b3d52cbc3201f7b193e350fbe59760` |
| `backend/src/app/apis/entities/session_task_update/sql/002_reference_session_id.sql` | `73a5b96119235ec47105b6d918874a63ddb723cf98434dab7e722384f3456467` |
| `backend/src/app/apis/entities/session_task_update/sql/003_reference_menu_item_id.sql` | `42657c3b816bba623f330c373d35b2480ebafbb4a16ec449a0c244269aa8d465` |
| `backend/src/app/apis/entities/shopping_item_create/sql/001_create.sql` | `be2667e82206b84dd9528d7fcae73c9d20d75f37b40d6cbdc2d4878a101f3ae6` |
| `backend/src/app/apis/entities/shopping_item_create/sql/002_reference_session_id.sql` | `73a5b96119235ec47105b6d918874a63ddb723cf98434dab7e722384f3456467` |
| `backend/src/app/apis/entities/shopping_item_create/sql/003_reference_total_id.sql` | `3034942539379d2d3c46e32df365854f2fb6669e19c419a47485a54278967cc2` |
| `backend/src/app/apis/entities/shopping_item_delete/sql/001_delete.sql` | `00202f77d7140a9844ac37b0bc5bad7e4db08bb9fcdf2c4650c492034a98ff6d` |
| `backend/src/app/apis/entities/shopping_item_get/sql/001_get.sql` | `0d3fe7f8fabe0295c33a28b920edf2b36565ca94baff03100610fad624494104` |
| `backend/src/app/apis/entities/shopping_item_list/sql/001_list.sql` | `5fb214dfebf4af58b6fbe55b03654c59dcd559ad52bb8f0511935eeb930fe4c1` |
| `backend/src/app/apis/entities/shopping_item_update/sql/001_update.sql` | `2ce94d8c30899156efa1f5ff178349b0bf12360d0bbdfac52f1de240942aae8a` |
| `backend/src/app/apis/entities/shopping_item_update/sql/002_reference_session_id.sql` | `73a5b96119235ec47105b6d918874a63ddb723cf98434dab7e722384f3456467` |
| `backend/src/app/apis/entities/shopping_item_update/sql/003_reference_total_id.sql` | `3034942539379d2d3c46e32df365854f2fb6669e19c419a47485a54278967cc2` |
| `backend/src/app/apis/entities/source_record_create/sql/001_create.sql` | `e4af46f81913d81cbac2a682ed375c55527255774947124cd15d192f594e75ee` |
| `backend/src/app/apis/entities/source_record_get/sql/001_get.sql` | `05ab88214925bb94999e5b23e93a864bf5428e1554548275fe7a3337d556251e` |
| `backend/src/app/apis/entities/source_record_list/sql/001_list.sql` | `4131d9d32fcce9dc1ed58495eed2fc07b08bd7ec02f5e1826152df9008cecd5d` |
| `backend/src/app/apis/entities/source_record_update/sql/001_update.sql` | `1b2696030ad5b7ff468a9712ebc262b662897c999269b3742045d040adb49a04` |
| `backend/src/app/apis/entities/step_dependency_create/sql/001_create.sql` | `a3ff99ee62e7d5da2761d6be6d01eed845354356c894593a68942284a25fb3ac` |
| `backend/src/app/apis/entities/step_dependency_get/sql/001_get.sql` | `676152faad6d8af132a7fd224f8947a9fafd9887863ff463298d67358694797f` |
| `backend/src/app/apis/entities/step_dependency_list/sql/001_list.sql` | `fbba91b0cf94a0130542b9ab5cd095d09f048fb75be895ad47155c382e18e0d7` |
| `backend/src/app/apis/entities/step_dependency_update/sql/001_update.sql` | `21a07e909e3ab8187fb5f53f206872ca9095ffd4d8d2623b5d4d7fceeb53f37d` |
| `backend/src/app/apis/entities/step_input_create/sql/001_create.sql` | `3d1d05656ecb46c5d70fbf6fa4a1b8e5441207773fe1e54a3787f8b982ecd542` |
| `backend/src/app/apis/entities/step_input_get/sql/001_get.sql` | `eb65abe6df836099c3eca5f96cf72ca2ccbfa2dfc7066c14142f5a69bd9fb87f` |
| `backend/src/app/apis/entities/step_input_list/sql/001_list.sql` | `6025788b54dac4e82c43ba995ebc4c89464af4b9ef94f75c8a9ba8f306853aad` |
| `backend/src/app/apis/entities/step_input_update/sql/001_update.sql` | `95ddd3f92d2bbcbc4bc2f852edf2d01b484786b56f8975319183f58db465d2a0` |
| `backend/src/app/apis/entities/step_media_create/sql/001_create.sql` | `66e8c38a9066728132ce75a3ddd3ef34daf4b7bce15aa895e6e4ca0cadb0c312` |
| `backend/src/app/apis/entities/step_media_get/sql/001_get.sql` | `2db1a3061ff562e77d7aeef0bf7ec7cffa0644d5cafe6e40258ab31d3af7a0ea` |
| `backend/src/app/apis/entities/step_media_list/sql/001_list.sql` | `19564d40842e50e6925b2cadd79657ce56ea98e9461bfa4646272a03f32a17ad` |
| `backend/src/app/apis/entities/step_media_update/sql/001_update.sql` | `5ebdaf460ec3be6b2c2f226148143636dd3fe5d2a6df16e9e011490213e87eb5` |
| `backend/src/app/apis/entities/step_parameter_create/sql/001_create.sql` | `95e81b357400eb7f822505d2798aa589ef08a93fd954e82d4de5c246095ec143` |
| `backend/src/app/apis/entities/step_parameter_get/sql/001_get.sql` | `158810ae1b8866789be40235cfb42f4de7e810e4037c7151d38f13272883ca2e` |
| `backend/src/app/apis/entities/step_parameter_list/sql/001_list.sql` | `5da8ea25adb57703d396c87947ba4d723ca06430d959b34a5aaa347c7aa7712c` |
| `backend/src/app/apis/entities/step_parameter_update/sql/001_update.sql` | `ab576ee57b82c55dab1af73f1f6a579e4ef9c6ccecba72e9a07bbd8113ff7b9c` |
| `backend/src/app/apis/entities/step_resource_create/sql/001_create.sql` | `dc3a8f96f699450ed183bed03d4eba0ea23eca5891f687fd6012b66f0fda79cd` |
| `backend/src/app/apis/entities/step_resource_get/sql/001_get.sql` | `11ca8383df66eaac14055b2cd53c0748a10fdbc1b23381b542d6ad8bf1073709` |
| `backend/src/app/apis/entities/step_resource_list/sql/001_list.sql` | `9c54df08008b2c42b436b8aa2188b2a991f85f5b81c263935df278b803f965fb` |
| `backend/src/app/apis/entities/step_resource_update/sql/001_update.sql` | `fe18e0e2ca5d8f5cd54ae4c48de8090058b7d2b6047e1c86248f8141f461ad25` |
| `backend/src/app/apis/entities/task_dependency_create/sql/001_create.sql` | `091c22ff339efb0cdf8fda26d310ca5738d68e0aa7754af47f703115c4f16ddd` |
| `backend/src/app/apis/entities/task_dependency_create/sql/002_reference_before_task_id.sql` | `b4d2fadb4db4cdb9fa656f5bf72e16c0fca491e6249721ca43bbdecaaa52bd12` |
| `backend/src/app/apis/entities/task_dependency_create/sql/003_reference_after_task_id.sql` | `b4d2fadb4db4cdb9fa656f5bf72e16c0fca491e6249721ca43bbdecaaa52bd12` |
| `backend/src/app/apis/entities/task_dependency_delete/sql/001_delete.sql` | `ec2443db0ce9a99fead3a63d3d5d59daa9789477e29e5d2356ab9ece4cffea81` |
| `backend/src/app/apis/entities/task_dependency_get/sql/001_get.sql` | `250a478a09caecedbd3129e3b0ad4c9d937f5160a011a6a8a0855f333c189b55` |
| `backend/src/app/apis/entities/task_dependency_list/sql/001_list.sql` | `42a86a3ea875573161dfc07ca42ddaa9905f3bed57053ca77d8889c6e20260e0` |
| `backend/src/app/apis/entities/task_dependency_update/sql/001_update.sql` | `b58c2a7922e3ce5541b4d80eb1b7a60fdcb9c570876afbe6748abab6013f2f32` |
| `backend/src/app/apis/entities/task_dependency_update/sql/002_reference_before_task_id.sql` | `b4d2fadb4db4cdb9fa656f5bf72e16c0fca491e6249721ca43bbdecaaa52bd12` |
| `backend/src/app/apis/entities/task_dependency_update/sql/003_reference_after_task_id.sql` | `b4d2fadb4db4cdb9fa656f5bf72e16c0fca491e6249721ca43bbdecaaa52bd12` |
| `backend/src/app/apis/entities/unit_create/sql/001_create.sql` | `01bf8ce485092166a8ea21ec61a41333a859e3492d23b774ea47700067f177a2` |
| `backend/src/app/apis/entities/unit_get/sql/001_get.sql` | `6d5c95eb5c92f597a24895a77bae1c0ee7f405cc8e981b303e3704c1ea75573f` |
| `backend/src/app/apis/entities/unit_list/sql/001_list.sql` | `4c1bc21ba1e3e75aefea364466c3481511e1407b132fdb0e26faa8e50df8ffc4` |
| `backend/src/app/apis/entities/unit_update/sql/001_update.sql` | `1cb4c3644cb96a58676f417fad2469cbadc7827e0c9de9cd6b167d88a7c22781` |
| `backend/src/app/apis/entities/user_exclusion_create/sql/001_create.sql` | `d0c9f1274963681d98ee2158157d8d90ea73c3c7c4de88e3f56606d2b696458b` |
| `backend/src/app/apis/entities/user_exclusion_create/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/user_exclusion_delete/sql/001_delete.sql` | `c1a8af8f9a3a59fce1ecbec8c00817f7509fd253116edfedf2b9fe3e826d9add` |
| `backend/src/app/apis/entities/user_exclusion_get/sql/001_get.sql` | `5a1355666bf09a87279fd2e18cd774a5dd0eaddd44cea71f194f8fa9afd94ef9` |
| `backend/src/app/apis/entities/user_exclusion_list/sql/001_list.sql` | `72a798ff5cc9fb5b21e0ae4640009c61ebb042fd3570be07b51b887406da6b3e` |
| `backend/src/app/apis/entities/user_exclusion_update/sql/001_update.sql` | `0a171e6c6f75afd66f93de01e1f351865222e3b6c47b908a7ab43742a1efb774` |
| `backend/src/app/apis/entities/user_exclusion_update/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/user_food_create/sql/001_create.sql` | `c75336bd2f9b4ae52db51461bbf5eef52d46f8ebf5241d9e581e39af80e6351a` |
| `backend/src/app/apis/entities/user_food_create/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/user_food_delete/sql/001_delete.sql` | `2f17ad88e201b467d99bdcc9aa153e4c1a93711be8bd7be0f9ce423e5ca0e2e0` |
| `backend/src/app/apis/entities/user_food_get/sql/001_get.sql` | `3ef3d29fb021241fd2bdabbb365f39ca2f7351a056f1005a6af93bf7549083a9` |
| `backend/src/app/apis/entities/user_food_list/sql/001_list.sql` | `833ed041dd90fefd7f65a505014ad61e535d20589c79cb8738f8a68c121b0d73` |
| `backend/src/app/apis/entities/user_food_update/sql/001_update.sql` | `8d8e2c9e4a0d2d62a13e9d81c7c546e9e75d4474bccee2650f328eac0f17f05b` |
| `backend/src/app/apis/entities/user_food_update/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/user_pantry_food_create/sql/001_create.sql` | `f881a002f5b146c9f4063c24b3a8200e60bb772d13bc2b55c57134d4e20db6a5` |
| `backend/src/app/apis/entities/user_pantry_food_create/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/user_pantry_food_delete/sql/001_delete.sql` | `a176c67ce78adee450b5efb1dbb84ed2bbf8e6b17ccbd3dcc02c989d40896682` |
| `backend/src/app/apis/entities/user_pantry_food_get/sql/001_get.sql` | `3d3762c9b5936def03b0d73b03989107b9673ac1fa6b7759e551c9791dce5353` |
| `backend/src/app/apis/entities/user_pantry_food_list/sql/001_list.sql` | `4f28cc785100937c12a42d9a23bd8168e7c24208b3d09cc0a4b0c29ef6388fc5` |
| `backend/src/app/apis/entities/user_pantry_food_update/sql/001_update.sql` | `e7216a7c52cc9ba35524284364e59ed93e4812a6ffa0fa99e01a1090c027bdee` |
| `backend/src/app/apis/entities/user_pantry_food_update/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/user_preference_create/sql/001_create.sql` | `0e1f96029ed66e40e3d3f7ed7ab0d08eb2cae67ab6b6427de7b025c09ff3adcb` |
| `backend/src/app/apis/entities/user_preference_create/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/user_preference_delete/sql/001_delete.sql` | `ede05a86da4736bab7c6d99b7bc509eb04daac3aac7ce6522c870889ed815ece` |
| `backend/src/app/apis/entities/user_preference_get/sql/001_get.sql` | `0b70461866a20e272fbb918a6264221efadd8bd4fd7c91622336e0b25acba05c` |
| `backend/src/app/apis/entities/user_preference_list/sql/001_list.sql` | `a1715d491fd7b4484728cb94e789c4e9fdb63c7d9f87817c1249b15f75816941` |
| `backend/src/app/apis/entities/user_preference_update/sql/001_update.sql` | `80b2a1a99211d19197a6b110d04325b641aedb45eb993946db5c6ab261ba2006` |
| `backend/src/app/apis/entities/user_preference_update/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/user_recipe_event_create/sql/001_create.sql` | `2336de9bf06dd3c19bbc3a7462b5f64b59789eea74ec4fd605b8335732e8c440` |
| `backend/src/app/apis/entities/user_recipe_event_create/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/user_recipe_event_create/sql/003_reference_recipe_version_id.sql` | `ecd6085d7f005353af0c3ccda7e5e73170f30de1385d9ce845a310599d23d8fa` |
| `backend/src/app/apis/entities/user_recipe_event_delete/sql/001_delete.sql` | `032a049f5f51c7f8e04f848feb3377038b3e73fec9686b58f5d57f98da337fd4` |
| `backend/src/app/apis/entities/user_recipe_event_get/sql/001_get.sql` | `ba72f30a7ff06678684c52086258b662cfb8d472ea1b386b4dd0daf07f5a8d7c` |
| `backend/src/app/apis/entities/user_recipe_event_list/sql/001_list.sql` | `91100488032497d0499d142d905b4b3bf5f3f48f925a91280eceb5881f70dd66` |
| `backend/src/app/apis/entities/user_shopping_check_create/sql/001_create.sql` | `417a6ebbeacc2f9c118cdf56a13c184fb0d36c1ef78d708efcf2a8d3efd9f3aa` |
| `backend/src/app/apis/entities/user_shopping_check_create/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/user_shopping_check_delete/sql/001_delete.sql` | `b900404f116ad898946637fec92ac23b9934b381587a74fd74a0e984ab652c6a` |
| `backend/src/app/apis/entities/user_shopping_check_get/sql/001_get.sql` | `3335f3b364e2cfd2413831737d5700e32332ca1c6d01386c771d469700d4a522` |
| `backend/src/app/apis/entities/user_shopping_check_list/sql/001_list.sql` | `b79a5346d61366c1cebfefac3c466c6ff76672d04af744a018e885126d356a1f` |
| `backend/src/app/apis/entities/user_shopping_check_update/sql/001_update.sql` | `1fc8f0971303fd2ec4566578893a731de74d7a6d9e4b37c2adc983dde71b9eee` |
| `backend/src/app/apis/entities/user_shopping_check_update/sql/002_reference_user_id.sql` | `40424fbff96fb3d261b5166d72e8a64e840e44a113491cb3bb7392285bac869a` |
| `backend/src/app/apis/entities/validation_result_create/sql/001_create.sql` | `2524a210283b438874b308656e52cc9f821bf78c25acff1ee849e557d32dbf7b` |
| `backend/src/app/apis/entities/validation_result_get/sql/001_get.sql` | `83c43f519526873c093af1c1e88c7110e6a8e562a7fe718175ac274d23a60038` |
| `backend/src/app/apis/entities/validation_result_list/sql/001_list.sql` | `1cea303676325a9c56b8c694d2f4a17ec024d82765585b0daeef361cc8d788c3` |
| `backend/src/app/apis/entities/workspace_revision_get/sql/001_get.sql` | `4827d3e2819f667c8a1f78c71c2a3127be01d4e17e3c76ff98b5c2da294d377a` |
| `backend/src/app/apis/entities/workspace_revision_list/sql/001_list.sql` | `f6caaabb2063249fd1715bcc777927bf29031c5c413005b75641b07bad53fe67` |
| `backend/src/app/apis/foods/list_foods/sql/001_select_foods.sql` | `881760b7a5ab42fd517ef1d368eda1748a5cf53aac60222f1fe6c5e3c2c7ad07` |
| `backend/src/app/apis/generation/advance_shard/sql/001_execute.sql` | `4b1ced2272ecb5a40179c943f7faa1669eaaafd5b8e571c54e9684afa106a3fc` |
| `backend/src/app/apis/generation/claim_shard/sql/001_execute.sql` | `dbe6301db87dd66ad68a1fd7e673f43ad5146a44f12cf19c55dfef839ef625b8` |
| `backend/src/app/apis/generation/renew_shard/sql/001_execute.sql` | `4d26a593cbe54b19e502877ce997c2603bdf52c84155d09019b7ad9520633628` |
| `backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql` | `1c59e45b6a3bb79ea02939835475817cbde5bce45d684c5c795d98adac5ae2c7` |
| `backend/src/app/apis/recipes/list_recipes/sql/001_select_recipes.sql` | `a6fc413af317bd340c6e57c41b4eb55a394b060170ff048eed3b5c53b3a512f9` |
| `backend/src/app/apis/recipes/random_recipe/sql/001_random_recipe.sql` | `96a100378f3b04b7265b1c0d3eb6efd1dd20e9b77c7e500f8cec658cc68fb3ec` |
| `backend/src/app/apis/workspace/add_menu_item/sql/q010_recipe.sql` | `6dc9a8255dfd42bf4b88dbd7a52b0a0c2a5ad640ebd1ed213546c968a3e2b10b` |
| `backend/src/app/apis/workspace/add_menu_item/sql/q011_ingredients.sql` | `d070a791fb8b735b33e7837f9be4c78e35547d7c5d44934f6771fc6b79d0feae` |
| `backend/src/app/apis/workspace/add_menu_item/sql/q012_menu.sql` | `6eee3b93a52dc8ad30be9b0ddba407b44e0c80a99999616ef69f600801adabe7` |
| `backend/src/app/apis/workspace/add_menu_item/sql/q013_insert_item.sql` | `c80accf722ff53d66e4ba7e320e165d6b9110ee2cdda67b0066a224676df8b83` |
| `backend/src/app/apis/workspace/add_menu_item/sql/q014_override.sql` | `063c035974dddd3b6a6520c02a39d23acee182fd7d6764586fd5013b2d51944f` |
| `backend/src/app/apis/workspace/add_menu_item/sql/q015_advance_menu.sql` | `1917adb8a95a88eac63653140294a92e33ab1099358814644f1ceb514e9a4730` |
| `backend/src/app/apis/workspace/add_menu_item/sql/q900_lock_revision.sql` | `f1ef00c3a47468641d44c89026381c3693e9cfc4462f18c18389931fcadaa63c` |
| `backend/src/app/apis/workspace/add_menu_item/sql/q901_advance_revision.sql` | `942c0db60727dc0731b1e3086d8313068f57c864b3322861e0a28bd62377e22f` |
| `backend/src/app/apis/workspace/add_menu_item/sql/q902_append_audit.sql` | `76db90e062480e68582345fe8aea09a91db366c547ac1195cb53b79c8e0a3346` |
| `backend/src/app/apis/workspace/commit_receipt/sql/q001_resolve_form.sql` | `95e901428a70edd6cf5331a8b460146875bbacd9411e9570bb7dd255cf67226e` |
| `backend/src/app/apis/workspace/commit_receipt/sql/q002_insert_lot.sql` | `d9ee914fbe437c2954cfc81cfd9b111b5ccb933f8a2a5b20b0af66ffca3d2908` |
| `backend/src/app/apis/workspace/commit_receipt/sql/q003_duplicate.sql` | `a6401ae24ce5731ec3a300aea0cf714428d289d2da7b7b2d9b3b22e1ea6097fe` |
| `backend/src/app/apis/workspace/commit_receipt/sql/q004_import.sql` | `6a37ae98b3d2041c798252d6351ec54df603756d2b5b65ed1e4826fe3b21c25a` |
| `backend/src/app/apis/workspace/commit_receipt/sql/q005_line.sql` | `af2eb8834b3b2b5aa4823da6cf94e87bd19100c288057e6bfb23af069c06353e` |
| `backend/src/app/apis/workspace/commit_receipt/sql/q019_private_release.sql` | `31dd774173a6d37241c56c29f6efcce28a76552c7fe4b9fed122483d17590b35` |
| `backend/src/app/apis/workspace/commit_receipt/sql/q020_custom_food.sql` | `80c1fc3305db0143b0db3f6585240eecf8e16f116bb6a443c2f352236fea576b` |
| `backend/src/app/apis/workspace/commit_receipt/sql/q021_custom_owner.sql` | `1160606c20a352ea612f82bd5701046444d33b128068a450da1c63f983ce396c` |
| `backend/src/app/apis/workspace/commit_receipt/sql/q022_custom_form.sql` | `636c931e95545a37ec3213d8527276399ef3468913e83b5f679b4e7d036d895a` |
| `backend/src/app/apis/workspace/commit_receipt/sql/q900_lock_revision.sql` | `f1ef00c3a47468641d44c89026381c3693e9cfc4462f18c18389931fcadaa63c` |
| `backend/src/app/apis/workspace/commit_receipt/sql/q901_advance_revision.sql` | `942c0db60727dc0731b1e3086d8313068f57c864b3322861e0a28bd62377e22f` |
| `backend/src/app/apis/workspace/commit_receipt/sql/q902_append_audit.sql` | `76db90e062480e68582345fe8aea09a91db366c547ac1195cb53b79c8e0a3346` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q001_current.sql` | `30ec6077ef4357122f120efc6402f2412080cf4349adf6c7668d161f9f4a0f8e` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q010_recipe.sql` | `6dc9a8255dfd42bf4b88dbd7a52b0a0c2a5ad640ebd1ed213546c968a3e2b10b` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q011_ingredients.sql` | `d070a791fb8b735b33e7837f9be4c78e35547d7c5d44934f6771fc6b79d0feae` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q012_menu.sql` | `6eee3b93a52dc8ad30be9b0ddba407b44e0c80a99999616ef69f600801adabe7` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q013_insert_item.sql` | `c80accf722ff53d66e4ba7e320e165d6b9110ee2cdda67b0066a224676df8b83` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q014_override.sql` | `063c035974dddd3b6a6520c02a39d23acee182fd7d6764586fd5013b2d51944f` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q015_advance_menu.sql` | `1917adb8a95a88eac63653140294a92e33ab1099358814644f1ceb514e9a4730` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q020_steps.sql` | `82003254031f8b26ae85bf7f8156528aef4c1319662f8143db2e30b974c50974` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q021_dependencies.sql` | `a98e864a40b465f7c483f5bd5b2bfbda8869ee588a307027b5e0f04f1460bba9` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q022_requirements.sql` | `9ffcd4fa296263a0fd7d5e2ef11a1ad34693ddc5589fbbdb9d152ad48cd16fd8` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q023_resources.sql` | `60dfff0563457c003fc06f4e425f889644c6db1cea8fe9884a8f610be0e140cf` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q024_ingredients.sql` | `f317f8008baab20827a26737068c88e7142daab26a0eb2978daa1c8331d70794` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q025_session.sql` | `00781c3bdc066d31fd235d397d3d4d2055742e55d14bf50227f217a9e4aaa1c7` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q026_task.sql` | `1613d24fee8aa4b61c34dd04ed01cd52b67c1e681eb0f7faa924c3c4cd0aae6c` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q027_dependency.sql` | `d987f7e62f97e3867f0ab965c76c3c2022abe45d5e1647c6fe2ef022c5139cb5` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q028_reservation.sql` | `21e1f4ae93406eff2d65350346f26b4d33df7813f3620e94e06ba20df95f34ed` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q029_total.sql` | `28975352341b96bb0f5591d63b55e5388f7504c0bb240c332288a03f3dcb2c97` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q030_menu_revision.sql` | `f163a89a593578147ad30117771d398140af6de98194edc75605b81e1078ff87` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q900_lock_revision.sql` | `f1ef00c3a47468641d44c89026381c3693e9cfc4462f18c18389931fcadaa63c` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q901_advance_revision.sql` | `942c0db60727dc0731b1e3086d8313068f57c864b3322861e0a28bd62377e22f` |
| `backend/src/app/apis/workspace/create_cooking_session/sql/q902_append_audit.sql` | `76db90e062480e68582345fe8aea09a91db366c547ac1195cb53b79c8e0a3346` |
| `backend/src/app/apis/workspace/create_custom_food/sql/q019_private_release.sql` | `31dd774173a6d37241c56c29f6efcce28a76552c7fe4b9fed122483d17590b35` |
| `backend/src/app/apis/workspace/create_custom_food/sql/q020_custom_food.sql` | `80c1fc3305db0143b0db3f6585240eecf8e16f116bb6a443c2f352236fea576b` |
| `backend/src/app/apis/workspace/create_custom_food/sql/q021_custom_owner.sql` | `1160606c20a352ea612f82bd5701046444d33b128068a450da1c63f983ce396c` |
| `backend/src/app/apis/workspace/create_custom_food/sql/q022_custom_form.sql` | `636c931e95545a37ec3213d8527276399ef3468913e83b5f679b4e7d036d895a` |
| `backend/src/app/apis/workspace/create_custom_food/sql/q900_lock_revision.sql` | `f1ef00c3a47468641d44c89026381c3693e9cfc4462f18c18389931fcadaa63c` |
| `backend/src/app/apis/workspace/create_custom_food/sql/q901_advance_revision.sql` | `942c0db60727dc0731b1e3086d8313068f57c864b3322861e0a28bd62377e22f` |
| `backend/src/app/apis/workspace/create_custom_food/sql/q902_append_audit.sql` | `76db90e062480e68582345fe8aea09a91db366c547ac1195cb53b79c8e0a3346` |
| `backend/src/app/apis/workspace/create_pantry_lot/sql/q001_resolve_form.sql` | `95e901428a70edd6cf5331a8b460146875bbacd9411e9570bb7dd255cf67226e` |
| `backend/src/app/apis/workspace/create_pantry_lot/sql/q002_insert_lot.sql` | `d9ee914fbe437c2954cfc81cfd9b111b5ccb933f8a2a5b20b0af66ffca3d2908` |
| `backend/src/app/apis/workspace/create_pantry_lot/sql/q900_lock_revision.sql` | `f1ef00c3a47468641d44c89026381c3693e9cfc4462f18c18389931fcadaa63c` |
| `backend/src/app/apis/workspace/create_pantry_lot/sql/q901_advance_revision.sql` | `942c0db60727dc0731b1e3086d8313068f57c864b3322861e0a28bd62377e22f` |
| `backend/src/app/apis/workspace/create_pantry_lot/sql/q902_append_audit.sql` | `76db90e062480e68582345fe8aea09a91db366c547ac1195cb53b79c8e0a3346` |
| `backend/src/app/apis/workspace/delete_menu_item/sql/q001_delete_item.sql` | `ad34c60fe50c5bcbb724ac2f812a3ae385094afa46db9d96e3837f86b3e01d41` |
| `backend/src/app/apis/workspace/delete_menu_item/sql/q900_lock_revision.sql` | `f1ef00c3a47468641d44c89026381c3693e9cfc4462f18c18389931fcadaa63c` |
| `backend/src/app/apis/workspace/delete_menu_item/sql/q901_advance_revision.sql` | `942c0db60727dc0731b1e3086d8313068f57c864b3322861e0a28bd62377e22f` |
| `backend/src/app/apis/workspace/delete_menu_item/sql/q902_append_audit.sql` | `76db90e062480e68582345fe8aea09a91db366c547ac1195cb53b79c8e0a3346` |
| `backend/src/app/apis/workspace/delete_pantry_lot/sql/q001_delete_lot.sql` | `c5cc28cf22b888ffe31265ff45e7e3cc9496366601afeb3e1061d500ab50d0e6` |
| `backend/src/app/apis/workspace/delete_pantry_lot/sql/q900_lock_revision.sql` | `f1ef00c3a47468641d44c89026381c3693e9cfc4462f18c18389931fcadaa63c` |
| `backend/src/app/apis/workspace/delete_pantry_lot/sql/q901_advance_revision.sql` | `942c0db60727dc0731b1e3086d8313068f57c864b3322861e0a28bd62377e22f` |
| `backend/src/app/apis/workspace/delete_pantry_lot/sql/q902_append_audit.sql` | `76db90e062480e68582345fe8aea09a91db366c547ac1195cb53b79c8e0a3346` |
| `backend/src/app/apis/workspace/get_workspace/sql/q001_revision.sql` | `3f175c5ab591190a122a59ab4110d6110d08ddfd8f715225fbc33faf7dd39b76` |
| `backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql` | `9b55454a113b56fb956a0957c1b547f3ab6baa2a27559509c164d584ec2ae4cc` |
| `backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql` | `62abd118bc364c94d0e8a913bf32e9e90eee4f3b630b1f92bf8c0b1f0c33af7c` |
| `backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql` | `9a5b175cd62d40357a8777c7315440e24d1a0db95e4413a5be86205bfd00f73c` |
| `backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql` | `52c30cf9391c0a045fd22e0dee8918ae68770ff78895f3a7be1e3de85e6e4cd9` |
| `backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql` | `74761a9be87f171bb68113911981ffec2378f041d5ee7989add4f0f95ce98f33` |
| `backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql` | `8895695343795f0816bccf7e0d06ddba7b2e90af5960afe19e614cf7617d8069` |
| `backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql` | `d99f03a815c631bde6930cfe65f7c93920f31d65a403826f6214efa05e413b21` |
| `backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql` | `9b9912f58fd1b54f8e991d3ffaa82011a371ead2f47fb0b8305e642485baa66d` |
| `backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql` | `8501e5fb67600ef7dd7c34111f2f1c86a32c93a30b1d73cff7dbaa826cc2506e` |
| `backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql` | `e1ca7f77863c8b79c88437d0e646bc3c7138247439875df88bb1479f4af34624` |
| `backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql` | `0f474bd79716f319c05be3e7288aa47617d77065fa55e33465a2a13d3b92f718` |
| `backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql` | `f6ed366fa2ff15dd7147993529dec399ed1a7defe21a012681df4966070026a7` |
| `backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql` | `4e4ff21f64f8d3bc5a7c0409009d3208854d2738b2e13018ce6e86c40b9bf504` |
| `backend/src/app/apis/workspace/preview_cooking_plan/sql/q001_steps.sql` | `b4efabef703588c6d2d52d127fb7ac9df80a7e1c0945f51c14a4c8db517f4c88` |
| `backend/src/app/apis/workspace/preview_cooking_plan/sql/q002_dependencies.sql` | `c2c8ab551635ef2b559ac4971956800919e9dcf5924d17205ffaa53586104533` |
| `backend/src/app/apis/workspace/preview_cooking_plan/sql/q003_requirements.sql` | `5fc4046c89f9c1f496de07207a322e5a0fb332e1ec2ce9cf8ec265dced7a96dc` |
| `backend/src/app/apis/workspace/preview_cooking_plan/sql/q004_resources.sql` | `60dfff0563457c003fc06f4e425f889644c6db1cea8fe9884a8f610be0e140cf` |
| `backend/src/app/apis/workspace/put_settings/sql/q001_clear_exclusion.sql` | `cdb1eb57166348a3ae6a37bece856d4711f41804c16eabd58b5b4b1dfcb12148` |
| `backend/src/app/apis/workspace/put_settings/sql/q002_clear_pantry.sql` | `3414433f6226669f151f9cd8eb1ebb6776bdf098ba2d68e5828951b6b7723bc1` |
| `backend/src/app/apis/workspace/put_settings/sql/q003_clear_equipment.sql` | `ce8cc60afee119b914a2e4b05998686aa6c7a737106d72e01728a7da8cad0dd1` |
| `backend/src/app/apis/workspace/put_settings/sql/q004_exclusion.sql` | `46088b79a4e709dbf275e29a103efeb64e6f2938524c5d2ae917c9c9cbaf0012` |
| `backend/src/app/apis/workspace/put_settings/sql/q005_pantry.sql` | `81b83568c7fc603f0a285b3cd3cbf03237d9b34a22f022a04ca514445e45deb3` |
| `backend/src/app/apis/workspace/put_settings/sql/q006_equipment.sql` | `ed46cdb08d3473d847048df16b0e699f8169501398d263c9712e1cbc5888c96a` |
| `backend/src/app/apis/workspace/put_settings/sql/q007_add_equipment.sql` | `4cbc0c76ef1057620d45ff5d855c2bc8784c161e8c1e1dabbd23cab9db88171b` |
| `backend/src/app/apis/workspace/put_settings/sql/q900_lock_revision.sql` | `f1ef00c3a47468641d44c89026381c3693e9cfc4462f18c18389931fcadaa63c` |
| `backend/src/app/apis/workspace/put_settings/sql/q901_advance_revision.sql` | `942c0db60727dc0731b1e3086d8313068f57c864b3322861e0a28bd62377e22f` |
| `backend/src/app/apis/workspace/put_settings/sql/q902_append_audit.sql` | `76db90e062480e68582345fe8aea09a91db366c547ac1195cb53b79c8e0a3346` |
| `backend/src/app/apis/workspace/put_shopping_checks/sql/q001_clear.sql` | `d9bd5d33ec5dc62c4063d46a49707df06491dc7236f19859bd8bd0af04649187` |
| `backend/src/app/apis/workspace/put_shopping_checks/sql/q002_insert.sql` | `3d4949477bec1b07b53fc6efbed3a9ce5e9563e14966f1108658ce8a76ff04da` |
| `backend/src/app/apis/workspace/put_shopping_checks/sql/q900_lock_revision.sql` | `f1ef00c3a47468641d44c89026381c3693e9cfc4462f18c18389931fcadaa63c` |
| `backend/src/app/apis/workspace/put_shopping_checks/sql/q901_advance_revision.sql` | `942c0db60727dc0731b1e3086d8313068f57c864b3322861e0a28bd62377e22f` |
| `backend/src/app/apis/workspace/put_shopping_checks/sql/q902_append_audit.sql` | `76db90e062480e68582345fe8aea09a91db366c547ac1195cb53b79c8e0a3346` |
| `backend/src/app/apis/workspace/save_recipe/sql/q001_recipe.sql` | `a7b23af452bb18355a2204998fa0223b909442d9d529752935c4935c600dc060` |
| `backend/src/app/apis/workspace/save_recipe/sql/q002_event.sql` | `9b13ab38aa16b8fbc6baf41d8d82ca10c5f4a708ecdeabed4b740e61e1a888b7` |
| `backend/src/app/apis/workspace/save_recipe/sql/q900_lock_revision.sql` | `f1ef00c3a47468641d44c89026381c3693e9cfc4462f18c18389931fcadaa63c` |
| `backend/src/app/apis/workspace/save_recipe/sql/q901_advance_revision.sql` | `942c0db60727dc0731b1e3086d8313068f57c864b3322861e0a28bd62377e22f` |
| `backend/src/app/apis/workspace/save_recipe/sql/q902_append_audit.sql` | `76db90e062480e68582345fe8aea09a91db366c547ac1195cb53b79c8e0a3346` |
| `backend/src/app/apis/workspace/undo_receipt/sql/q001_import.sql` | `1c7bc1e7e8cd4ff44d7d9cfd65dd8ca19c51c3166c38ced44acf9521c28a91bb` |
| `backend/src/app/apis/workspace/undo_receipt/sql/q002_eligible_lots.sql` | `40c08978127d8527381e87538932ff53e13158dc8a2cd06104aee8d94ce67e20` |
| `backend/src/app/apis/workspace/undo_receipt/sql/q003_revert.sql` | `1e387fb569a77b51c9adc387f4b34dd81e7fe492a46d46d9f013b1612afa7f86` |
| `backend/src/app/apis/workspace/undo_receipt/sql/q900_lock_revision.sql` | `f1ef00c3a47468641d44c89026381c3693e9cfc4462f18c18389931fcadaa63c` |
| `backend/src/app/apis/workspace/undo_receipt/sql/q901_advance_revision.sql` | `942c0db60727dc0731b1e3086d8313068f57c864b3322861e0a28bd62377e22f` |
| `backend/src/app/apis/workspace/undo_receipt/sql/q902_append_audit.sql` | `76db90e062480e68582345fe8aea09a91db366c547ac1195cb53b79c8e0a3346` |
| `backend/src/app/apis/workspace/unsave_recipe/sql/q001_recipe.sql` | `a7b23af452bb18355a2204998fa0223b909442d9d529752935c4935c600dc060` |
| `backend/src/app/apis/workspace/unsave_recipe/sql/q002_event.sql` | `1537a6db8222a11038e9a33f0a818e7cd244b9a3c4e4dd80ebf0a8895c9c24cf` |
| `backend/src/app/apis/workspace/unsave_recipe/sql/q900_lock_revision.sql` | `f1ef00c3a47468641d44c89026381c3693e9cfc4462f18c18389931fcadaa63c` |
| `backend/src/app/apis/workspace/unsave_recipe/sql/q901_advance_revision.sql` | `942c0db60727dc0731b1e3086d8313068f57c864b3322861e0a28bd62377e22f` |
| `backend/src/app/apis/workspace/unsave_recipe/sql/q902_append_audit.sql` | `76db90e062480e68582345fe8aea09a91db366c547ac1195cb53b79c8e0a3346` |
| `backend/src/app/apis/workspace/update_cooking_session/sql/q001_current.sql` | `30ec6077ef4357122f120efc6402f2412080cf4349adf6c7668d161f9f4a0f8e` |
| `backend/src/app/apis/workspace/update_cooking_session/sql/q002_tasks.sql` | `b8e78720fbc3c5efaa7505e50ab304aeb6e9e03e07d5b59794570dd57c572052` |
| `backend/src/app/apis/workspace/update_cooking_session/sql/q003_progress.sql` | `838010cb9e29f5f2c6de040b0749549efe068917c2cabd30f442ffba76db9aac` |
| `backend/src/app/apis/workspace/update_cooking_session/sql/q004_complete_task.sql` | `a7d1bbda58224d93ce914c3afbff9eb2a1bf169ca5ae1ecd577642d3c5fe1f81` |
| `backend/src/app/apis/workspace/update_cooking_session/sql/q005_timer.sql` | `6f359f4307d38f98cf56a1770221e375a261097164e763bd8194b82261ff360c` |
| `backend/src/app/apis/workspace/update_cooking_session/sql/q006_totals.sql` | `664f398c861b8933385571c0f05823a4cb2fee31db3dccd0d7c329dc1453666f` |
| `backend/src/app/apis/workspace/update_cooking_session/sql/q007_available.sql` | `75cd65561911bb1f6dbc6eed0fc23b13d9ba8f5281305046f6bb16927a59891f` |
| `backend/src/app/apis/workspace/update_cooking_session/sql/q008_consume.sql` | `2bb3bc45473bcde2d0919d5e9a8611096db7800ad3651ace1cc7448bd4b2bef6` |
| `backend/src/app/apis/workspace/update_cooking_session/sql/q009_ledger.sql` | `c23371014c55685a4ce5275660e10eee0df33f669acfb38edbf0d93c3a8215fc` |
| `backend/src/app/apis/workspace/update_cooking_session/sql/q010_outcome.sql` | `e04d8c790f4f7fade76c1af53dea02351c16913dcaaf47be32dca6a9a936a259` |
| `backend/src/app/apis/workspace/update_cooking_session/sql/q900_lock_revision.sql` | `f1ef00c3a47468641d44c89026381c3693e9cfc4462f18c18389931fcadaa63c` |
| `backend/src/app/apis/workspace/update_cooking_session/sql/q901_advance_revision.sql` | `942c0db60727dc0731b1e3086d8313068f57c864b3322861e0a28bd62377e22f` |
| `backend/src/app/apis/workspace/update_cooking_session/sql/q902_append_audit.sql` | `76db90e062480e68582345fe8aea09a91db366c547ac1195cb53b79c8e0a3346` |
| `backend/src/app/apis/workspace/update_menu_item/sql/q001_delete_item.sql` | `ad34c60fe50c5bcbb724ac2f812a3ae385094afa46db9d96e3837f86b3e01d41` |
| `backend/src/app/apis/workspace/update_menu_item/sql/q010_recipe.sql` | `6dc9a8255dfd42bf4b88dbd7a52b0a0c2a5ad640ebd1ed213546c968a3e2b10b` |
| `backend/src/app/apis/workspace/update_menu_item/sql/q011_ingredients.sql` | `d070a791fb8b735b33e7837f9be4c78e35547d7c5d44934f6771fc6b79d0feae` |
| `backend/src/app/apis/workspace/update_menu_item/sql/q012_menu.sql` | `6eee3b93a52dc8ad30be9b0ddba407b44e0c80a99999616ef69f600801adabe7` |
| `backend/src/app/apis/workspace/update_menu_item/sql/q013_insert_item.sql` | `c80accf722ff53d66e4ba7e320e165d6b9110ee2cdda67b0066a224676df8b83` |
| `backend/src/app/apis/workspace/update_menu_item/sql/q014_override.sql` | `063c035974dddd3b6a6520c02a39d23acee182fd7d6764586fd5013b2d51944f` |
| `backend/src/app/apis/workspace/update_menu_item/sql/q015_advance_menu.sql` | `1917adb8a95a88eac63653140294a92e33ab1099358814644f1ceb514e9a4730` |
| `backend/src/app/apis/workspace/update_menu_item/sql/q900_lock_revision.sql` | `f1ef00c3a47468641d44c89026381c3693e9cfc4462f18c18389931fcadaa63c` |
| `backend/src/app/apis/workspace/update_menu_item/sql/q901_advance_revision.sql` | `942c0db60727dc0731b1e3086d8313068f57c864b3322861e0a28bd62377e22f` |
| `backend/src/app/apis/workspace/update_menu_item/sql/q902_append_audit.sql` | `76db90e062480e68582345fe8aea09a91db366c547ac1195cb53b79c8e0a3346` |
| `backend/src/app/apis/workspace/update_pantry_lot/sql/q001_resolve_form.sql` | `95e901428a70edd6cf5331a8b460146875bbacd9411e9570bb7dd255cf67226e` |
| `backend/src/app/apis/workspace/update_pantry_lot/sql/q002_update_lot.sql` | `fa7a63f0126e3da9d7412f88db22be6600619e7509dd0cf7732bccd18c6b839d` |
| `backend/src/app/apis/workspace/update_pantry_lot/sql/q900_lock_revision.sql` | `f1ef00c3a47468641d44c89026381c3693e9cfc4462f18c18389931fcadaa63c` |
| `backend/src/app/apis/workspace/update_pantry_lot/sql/q901_advance_revision.sql` | `942c0db60727dc0731b1e3086d8313068f57c864b3322861e0a28bd62377e22f` |
| `backend/src/app/apis/workspace/update_pantry_lot/sql/q902_append_audit.sql` | `76db90e062480e68582345fe8aea09a91db366c547ac1195cb53b79c8e0a3346` |
| `backend/src/app/entities/sql/audit.sql` | `83f5e94b81bab01777a5d2c4de22d49690a7f3a5feb4c3618f8ac0d5c3bfe9cf` |
| `backend/src/app/entities/sql/outbox.sql` | `bed9ba25493683ae26b58cdf3e34438d33d279c70ed0a6e0f379153f759d8530` |
| `backend/src/app/entities/sql/workspace.sql` | `1a7ee0689608703599fe173b0fd0643dfd17494857631c7cab88c3de48e83d09` |
| `database/migrations/001_user_state.sql` | `4f085833e9d63238900f9b3a7be1356fe5bb05e56bc93b276ffa32a139cc20f4` |
| `database/migrations/002_relational_schema.sql` | `200d0fafcf31fd09850298d735df4af06b6556b3f6df4c5ba2c8636a8d39cb90` |
| `database/migrations/003_service_operations.sql` | `4797f6c116c7872f52f96a5f05ecab70a5386b10603c662877d1988bc947015a` |
| `database/migrations/004_backup_restore.sql` | `5e07c5e123f78fa1721647635dbb56af318d9c9948b46d8ae3019edf6a54ebca` |
| `database/migrations/005_manual_duration.sql` | `4c42721e70692842d3ba14abbaea7e75b26d1e01314f2fbf2730f543c5102e6c` |

## CDK合成資源

以下は合成テンプレートの資源定義。アカウントへの作成結果ではない。

### Data

| 資源種別 | 数 |
|---|---|
| `AWS::Cognito::UserPool` | 1 |
| `AWS::Cognito::UserPoolClient` | 1 |
| `AWS::Cognito::UserPoolDomain` | 1 |
| `AWS::EC2::EIP` | 1 |
| `AWS::EC2::InternetGateway` | 1 |
| `AWS::EC2::NatGateway` | 1 |
| `AWS::EC2::Route` | 4 |
| `AWS::EC2::RouteTable` | 6 |
| `AWS::EC2::SecurityGroup` | 2 |
| `AWS::EC2::SecurityGroupIngress` | 1 |
| `AWS::EC2::Subnet` | 6 |
| `AWS::EC2::SubnetRouteTableAssociation` | 6 |
| `AWS::EC2::VPC` | 1 |
| `AWS::EC2::VPCGatewayAttachment` | 1 |
| `AWS::RDS::DBCluster` | 1 |
| `AWS::RDS::DBClusterParameterGroup` | 1 |
| `AWS::RDS::DBInstance` | 2 |
| `AWS::RDS::DBSubnetGroup` | 1 |
| `AWS::SecretsManager::Secret` | 2 |
| `AWS::SecretsManager::SecretTargetAttachment` | 1 |

| Logical ID | 資源種別 |
|---|---|
| `ApplicationDatabaseSecretCC2242CC` | `AWS::SecretsManager::Secret` |
| `DatabaseClientsD3CE02C8` | `AWS::EC2::SecurityGroup` |
| `DatabaseVpc73869E3A` | `AWS::EC2::VPC` |
| `DatabaseVpcApplicationSubnet1DefaultRoute33B05C1E` | `AWS::EC2::Route` |
| `DatabaseVpcApplicationSubnet1RouteTable59AE27F4` | `AWS::EC2::RouteTable` |
| `DatabaseVpcApplicationSubnet1RouteTableAssociation7662CF55` | `AWS::EC2::SubnetRouteTableAssociation` |
| `DatabaseVpcApplicationSubnet1SubnetBA088685` | `AWS::EC2::Subnet` |
| `DatabaseVpcApplicationSubnet2DefaultRouteA63A60C7` | `AWS::EC2::Route` |
| `DatabaseVpcApplicationSubnet2RouteTableAssociation4BC54FB7` | `AWS::EC2::SubnetRouteTableAssociation` |
| `DatabaseVpcApplicationSubnet2RouteTableC66B9C88` | `AWS::EC2::RouteTable` |
| `DatabaseVpcApplicationSubnet2SubnetC27820DA` | `AWS::EC2::Subnet` |
| `DatabaseVpcDatabaseSubnet1RouteTable0D7AC03E` | `AWS::EC2::RouteTable` |
| `DatabaseVpcDatabaseSubnet1RouteTableAssociationCC05C285` | `AWS::EC2::SubnetRouteTableAssociation` |
| `DatabaseVpcDatabaseSubnet1Subnet7766E98F` | `AWS::EC2::Subnet` |
| `DatabaseVpcDatabaseSubnet2RouteTableAssociationDBE6669F` | `AWS::EC2::SubnetRouteTableAssociation` |
| `DatabaseVpcDatabaseSubnet2RouteTableF5DB4573` | `AWS::EC2::RouteTable` |
| `DatabaseVpcDatabaseSubnet2SubnetB02499AD` | `AWS::EC2::Subnet` |
| `DatabaseVpcIGWEE9AA335` | `AWS::EC2::InternetGateway` |
| `DatabaseVpcPublicSubnet1DefaultRouteE877A296` | `AWS::EC2::Route` |
| `DatabaseVpcPublicSubnet1EIPF94CE0DB` | `AWS::EC2::EIP` |
| `DatabaseVpcPublicSubnet1NATGatewayC9132240` | `AWS::EC2::NatGateway` |
| `DatabaseVpcPublicSubnet1RouteTable27CC5B0F` | `AWS::EC2::RouteTable` |
| `DatabaseVpcPublicSubnet1RouteTableAssociation7001A26C` | `AWS::EC2::SubnetRouteTableAssociation` |
| `DatabaseVpcPublicSubnet1Subnet991DEF06` | `AWS::EC2::Subnet` |
| `DatabaseVpcPublicSubnet2DefaultRoute0EFBC1D0` | `AWS::EC2::Route` |
| `DatabaseVpcPublicSubnet2RouteTable66A28D69` | `AWS::EC2::RouteTable` |
| `DatabaseVpcPublicSubnet2RouteTableAssociation9D517D4A` | `AWS::EC2::SubnetRouteTableAssociation` |
| `DatabaseVpcPublicSubnet2Subnet7DBD14C7` | `AWS::EC2::Subnet` |
| `DatabaseVpcVPCGW5AECC992` | `AWS::EC2::VPCGatewayAttachment` |
| `RecipeWeavedevDataRelationalClusterSecret567883473fdaad7efa858a3daf9490cf0a702aeb` | `AWS::SecretsManager::Secret` |
| `RelationalClusterC48CF721` | `AWS::RDS::DBCluster` |
| `RelationalClusterParameterGroup978A90AC` | `AWS::RDS::DBClusterParameterGroup` |
| `RelationalClusterReaderB42CF8CE` | `AWS::RDS::DBInstance` |
| `RelationalClusterSecretAttachmentFFD78493` | `AWS::SecretsManager::SecretTargetAttachment` |
| `RelationalClusterSecurityGroup831C7E01` | `AWS::EC2::SecurityGroup` |
| `RelationalClusterSecurityGroupfromRecipeWeavedevDataDatabaseClients6972F9BCIndirectPortF84FD0F5` | `AWS::EC2::SecurityGroupIngress` |
| `RelationalClusterSubnets22B4A7B4` | `AWS::RDS::DBSubnetGroup` |
| `RelationalClusterWriter39A8CC0D` | `AWS::RDS::DBInstance` |
| `Users0A0EEA89` | `AWS::Cognito::UserPool` |
| `UsersHostedLogin8DC3860C` | `AWS::Cognito::UserPoolDomain` |
| `UsersWebClient8EE36D42` | `AWS::Cognito::UserPoolClient` |

### Service

| 資源種別 | 数 |
|---|---|
| `AWS::ApiGatewayV2::Api` | 1 |
| `AWS::ApiGatewayV2::Integration` | 1 |
| `AWS::ApiGatewayV2::Route` | 1 |
| `AWS::ApiGatewayV2::Stage` | 1 |
| `AWS::CloudFront::CachePolicy` | 1 |
| `AWS::CloudFront::Distribution` | 1 |
| `AWS::CloudFront::OriginAccessControl` | 1 |
| `AWS::IAM::Policy` | 3 |
| `AWS::IAM::Role` | 3 |
| `AWS::Lambda::Function` | 3 |
| `AWS::Lambda::LayerVersion` | 1 |
| `AWS::Lambda::Permission` | 1 |
| `AWS::Logs::LogGroup` | 4 |
| `AWS::S3::Bucket` | 1 |
| `AWS::S3::BucketPolicy` | 1 |
| `Custom::CDKBucketDeployment` | 1 |

| Logical ID | 資源種別 |
|---|---|
| `ApiF70053CD` | `AWS::Lambda::Function` |
| `ApiLogs3D05D88B` | `AWS::Logs::LogGroup` |
| `ApiServiceRole1BD550DA` | `AWS::IAM::Role` |
| `ApiServiceRoleDefaultPolicyB24862FE` | `AWS::IAM::Policy` |
| `ApiStage` | `AWS::ApiGatewayV2::Stage` |
| `CustomCDKBucketDeployment8693BB64968944B69AAFB0CC9EB8756C81C01536` | `AWS::Lambda::Function` |
| `CustomCDKBucketDeployment8693BB64968944B69AAFB0CC9EB8756CServiceRole89A01265` | `AWS::IAM::Role` |
| `CustomCDKBucketDeployment8693BB64968944B69AAFB0CC9EB8756CServiceRoleDefaultPolicy88902FDF` | `AWS::IAM::Policy` |
| `DatabaseMigrationE6E8D266` | `AWS::Lambda::Function` |
| `DatabaseMigrationServiceRole901F66A1` | `AWS::IAM::Role` |
| `DatabaseMigrationServiceRoleDefaultPolicy261D10C5` | `AWS::IAM::Policy` |
| `DeployWebAwsCliLayer4A26D5E7` | `AWS::Lambda::LayerVersion` |
| `DeployWebCustomResource253E03A7` | `Custom::CDKBucketDeployment` |
| `HttpAccessLogs7ADEF396` | `AWS::Logs::LogGroup` |
| `HttpApiANYapiproxy20978A2B` | `AWS::ApiGatewayV2::Route` |
| `HttpApiANYapiproxyFastApiFEE741E4` | `AWS::ApiGatewayV2::Integration` |
| `HttpApiANYapiproxyFastApiPermission522144CC` | `AWS::Lambda::Permission` |
| `HttpApiF5A9A8A7` | `AWS::ApiGatewayV2::Api` |
| `MigrationLogs670D4322` | `AWS::Logs::LogGroup` |
| `StaticCache185A1D0E` | `AWS::CloudFront::CachePolicy` |
| `Web3C8945DB` | `AWS::CloudFront::Distribution` |
| `WebAssets27872646` | `AWS::S3::Bucket` |
| `WebAssetsPolicy59254521` | `AWS::S3::BucketPolicy` |
| `WebDeploymentLogs48919846` | `AWS::Logs::LogGroup` |
| `WebOrigin1S3OriginAccessControl98EE5C09` | `AWS::CloudFront::OriginAccessControl` |

## 再現と受入の境界

- 画面の型検査・状態計算テストと、APIの型検査・認証/競合テストを別々に実行する。
- OpenAPIとSQL wrapperは `app-docs --check`、本書は `--check` で追従を確認する。
- CDK構造検査と合成は配備前の検証。配備先のPostgreSQL実接続・Cognito実ログインは別の受入を要する。
- 現行の設計判断は [ADR-0002](../ADR-0002-relational-service.md)、初期構成の履歴は [ADR-0001](../ADR-0001-service-dev.md) を参照する。
