# テーブル仕様: recipeweave.outbox_event

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

検索・キャッシュ更新配信

定義元: `database/migrations/002_relational_schema.sql:statement-592`

| 列 | 型 | NULL許可 | 既定値 | 制約 | 意味 |
|---|---|---|---|---|---|
| id | uuid | 不可 | なし | PRIMARY KEY | 不変の行識別子 |
| created_at | timestamptz | 不可 | NOW() | なし | 作成日時（UTC） |
| event_type | text | 不可 | なし | LENGTH(BTRIM(event_type)) BETWEEN 1 AND 20000 | recipe_published/withdrawn/user_erased等 |
| aggregate_id | uuid | 不可 | なし | なし | 対象ID（配信対象でありFKでない） |
| payload | jsonb | 不可 | なし | payload IS NULL OR PG_COLUMN_SIZE(payload) &lt;= 1048576 | schema_version付き最小通知 |
| delivered_at | timestamptz | 可 | なし | なし | 配送完了 |
| attempt_count | integer | 不可 | なし | attempt_count &gt;= 0 | 再試行数 |

## 表制約

- `CHECK (attempt_count >= 0)`
- `CHECK (LENGTH(BTRIM(event_type)) BETWEEN 1 AND 20000)`
- `CHECK (payload IS NULL OR PG_COLUMN_SIZE(payload) <= 1048576)`
- `PRIMARY KEY (id)`

## 索引

| 名称 | 一意 | 定義 |
|---|---|---|
| ix_outbox_event_search_0 | False | ( created_at ) WHERE delivered_at IS NULL |

## 外部キー

外部キーなし。

保持・所属領域: transient / 運用

## 利用API

| operationId | CRUD | SQL |
|---|---|---|
| entity_outbox_event_get | R | backend/src/app/apis/entities/outbox_event_get/sql/001_get.sql |
| entity_outbox_event_list | R | backend/src/app/apis/entities/outbox_event_list/sql/001_list.sql |
| entity_source_record_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_source_record_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_catalog_release_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_catalog_release_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_unit_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_unit_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_food_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_food_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_food_alias_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_food_alias_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_food_form_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_food_form_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_conversion_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_conversion_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_form_yield_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_product_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_product_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_product_version_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_product_component_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_allergen_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_allergen_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_food_allergen_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_product_allergen_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_nutrient_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_nutrient_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_nutrition_fact_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_axis_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_axis_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_axis_option_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_axis_option_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_food_axis_option_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_food_axis_option_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_recipe_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_recipe_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_recipe_version_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_recipe_version_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_recipe_option_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_recipe_option_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_scaling_rule_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_scaling_point_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_recipe_ingredient_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_recipe_ingredient_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_operation_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_operation_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_operation_parameter_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_operation_parameter_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_recipe_step_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_recipe_step_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_step_parameter_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_step_parameter_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_material_node_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_material_node_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_step_input_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_step_input_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_step_dependency_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_step_dependency_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_resource_type_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_resource_type_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_step_resource_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_step_resource_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_media_asset_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_step_media_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_step_media_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_generation_policy_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_generation_job_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_generation_job_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_generation_choice_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_generation_choice_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_generation_food_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_generation_food_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_generation_result_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_compatibility_rule_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_validation_result_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_recipe_signature_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_recipe_similarity_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_recipe_similarity_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_product_preparation_rule_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_food_identity_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_food_identity_member_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_generation_template_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_generation_shard_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_candidate_attempt_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_candidate_attempt_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_recipe_embedding_create | C | backend/src/app/entities/sql/outbox.sql |
| entity_recipe_embedding_update | C | backend/src/app/entities/sql/outbox.sql |
| entity_generation_stratum_metric_create | C | backend/src/app/entities/sql/outbox.sql |
| advance_shard | C | backend/src/app/entities/sql/outbox.sql |
| claim_shard | C | backend/src/app/entities/sql/outbox.sql |
| renew_shard | C | backend/src/app/entities/sql/outbox.sql |
