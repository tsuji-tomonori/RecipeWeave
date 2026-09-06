# SQL仕様: export_backup

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## backend/src/app/apis/backup/export_backup/sql/q001_lock_revision.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.workspace_revision | R | revision, user_id |

バインド変数: actor_id

```sql
-- 本人の更新版をロックし、確認と置換の間の更新を検出する。
SELECT revision FROM recipeweave.workspace_revision
WHERE user_id = %(actor_id)s FOR UPDATE;
```

## backend/src/app/apis/backup/export_backup/sql/q002_profile.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.app_user | R | id, locale, timezone |

バインド変数: actor_id

```sql
-- 認証主体・状態を含めず、復元できる本人の表示設定だけを読む。
SELECT
    locale,
    timezone
FROM recipeweave.app_user
WHERE id = %(actor_id)s;
```

## backend/src/app/apis/backup/export_backup/sql/q010_export_tables.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.catalog_release | R | created_at, id, manifest_hash, owner_id, published_at, version |
| recipeweave.conversion | R | conditions, created_at, factor, form_id, from_unit_id, id, quality, release_id, source_id, to_unit_id |
| recipeweave.cooking_session | R | created_at, current_task_index, id, input_hash, input_snapshot, menu_id, menu_revision, planner_version, status, target_at |
| recipeweave.food | R | code, created_at, id, kind, name, owner_id, parent_id, release_id, status |
| recipeweave.food_alias | R | alias, created_at, food_id, id, locale |
| recipeweave.food_allergen | R | allergen_id, created_at, form_id, id, presence, source_id |
| recipeweave.food_axis_option | R | created_at, food_id, id, option_id |
| recipeweave.food_form | R | base_unit_id, created_at, food_id, id, name, quantity_basis, state, status |
| recipeweave.form_yield | R | conditions, created_at, id, input_form_id, output_form_id, quality, source_id, yield_ratio |
| recipeweave.ingredient_total | R | actual_amount, calculation_version, consumption_outcome, created_at, form_id, id, product_version_id, quality, required_amount, session_id, unit_id |
| recipeweave.kitchen_resource | R | active, capacity, created_at, id, name, quantity, resource_type_id, user_id |
| recipeweave.menu | R | created_at, id, name, revision, servings, user_id |
| recipeweave.menu_ingredient_override | R | amount, created_at, form_id, id, ingredient_line_id, menu_item_id, product_version_id, selected |
| recipeweave.menu_item | R | created_at, id, menu_id, position, recipe_version_id, role_option_id, servings |
| recipeweave.nutrition_fact | R | amount, basis_amount, basis_unit_id, created_at, form_id, id, nutrient_id, product_version_id, source_id |
| recipeweave.pantry_consumption | R | amount, created_at, id, lot_id, session_id, unit_id, user_id |
| recipeweave.pantry_lot | R | amount, created_at, edited, expires_on, form_id, id, location, opened_at, original_amount, original_form_id, original_unit_id, priority, product_version_id, quantity_quality, source_import_id, status, unit_id, updated_at, user_id |
| recipeweave.product | R | brand, created_at, food_id, gtin, id, name, status |
| recipeweave.product_allergen | R | allergen_id, created_at, id, presence, product_version_id, source_id |
| recipeweave.product_component | R | amount, created_at, form_id, id, name, product_version_id, quality, unit_id |
| recipeweave.product_preparation_rule | R | allowed, created_at, id, operation_id, parameter_contract, product_version_id, source_id, use_original_container |
| recipeweave.product_version | R | created_at, drain_amount, form_id, id, net_amount, preparation_note, product_id, source_id, unit_id, valid_from, version |
| recipeweave.receipt_import | R | committed_at, created_at, file_sha256, id, idempotency_key, reverted_at, revision, status, undo_preserved_count, user_id |
| recipeweave.receipt_line | R | amount, created_at, decision, form_id, id, import_id, line_no, pantry_lot_id, product_version_id, raw_name, unit_id |
| recipeweave.resource_reservation | R | created_at, end_s, id, quantity, resource_id, start_s, task_id |
| recipeweave.session_task | R | actual_end_at, actual_start_at, batch_no, confirmed_duration_s, created_at, duration_source, id, menu_item_id, planned_end_s, planned_start_s, session_id, status, step_id, timer_duration_s, timer_started_at |
| recipeweave.shopping_item | R | archived, checked, checked_at, client_key, created_at, id, net_shortage, package_count, product_version_id, session_id, surplus_amount, total_id |
| recipeweave.task_dependency | R | after_task_id, before_task_id, created_at, id, max_lag_s, min_lag_s, reason |
| recipeweave.user_exclusion | R | allergen_id, created_at, food_id, id, strict, user_id |
| recipeweave.user_food | R | created_at, food_id, id, user_id |
| recipeweave.user_pantry_food | R | created_at, food_id, id, user_id |
| recipeweave.user_preference | R | created_at, id, option_id, user_id, weight |
| recipeweave.user_recipe_event | R | created_at, id, kind, occurred_at, recipe_version_id, request_key, user_id |
| recipeweave.user_shopping_check | R | amount, archived, checked_at, created_at, food_id, id, key, signature, unit_id, user_id |

バインド変数: actor_id

```sql
-- 本人の業務行と私有食品の全列を一つの読取スナップショットで取得する。
SELECT
    (SELECT
        COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
            'id', t.id,
            'created_at', t.created_at,
            'user_id', t.user_id,
            'option_id', t.option_id,
            'weight', t.weight::TEXT
        ) ORDER BY t.id), '[]'::JSONB)
    FROM recipeweave.user_preference AS t
    WHERE (t.user_id = %(actor_id)s)) AS rows_user_preference,
    (SELECT
        COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
            'id', t.id,
            'created_at', t.created_at,
            'user_id', t.user_id,
            'food_id', t.food_id,
            'allergen_id', t.allergen_id,
            'strict', t.strict
        ) ORDER BY t.id), '[]'::JSONB)
    FROM recipeweave.user_exclusion AS t
    WHERE (t.user_id = %(actor_id)s)) AS rows_user_exclusion,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'user_id', t.user_id,
                'recipe_version_id', t.recipe_version_id,
                'kind', t.kind,
                'occurred_at', t.occurred_at,
                'request_key', t.request_key
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.user_recipe_event AS t
        WHERE (t.user_id = %(actor_id)s)
    ) AS rows_user_recipe_event,
    (SELECT
        COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
            'id', t.id,
            'created_at', t.created_at,
            'user_id', t.user_id,
            'name', t.name,
            'servings', t.servings::TEXT,
            'revision', t.revision
        ) ORDER BY t.id), '[]'::JSONB)
    FROM recipeweave.menu AS t
    WHERE (t.user_id = %(actor_id)s)) AS rows_menu,
    (SELECT
        COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
            'id', t.id,
            'created_at', t.created_at,
            'menu_id', t.menu_id,
            'recipe_version_id', t.recipe_version_id,
            'servings', t.servings::TEXT,
            'role_option_id', t.role_option_id,
            'position', t.position
        ) ORDER BY t.id), '[]'::JSONB)
    FROM recipeweave.menu_item AS t
    WHERE (EXISTS (
        SELECT owner_0.id
        FROM recipeweave.menu AS owner_0
        WHERE
            owner_0.id = t.menu_id
            AND owner_0.user_id = %(actor_id)s
    ))) AS rows_menu_item,
    (SELECT
        COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
            'id', t.id,
            'created_at', t.created_at,
            'menu_item_id', t.menu_item_id,
            'ingredient_line_id', t.ingredient_line_id,
            'selected', t.selected,
            'amount', t.amount::TEXT,
            'form_id', t.form_id,
            'product_version_id', t.product_version_id
        ) ORDER BY t.id), '[]'::JSONB)
    FROM recipeweave.menu_ingredient_override AS t
    WHERE (EXISTS (
        SELECT owner_0.id
        FROM recipeweave.menu_item AS owner_0
        WHERE
            owner_0.id = t.menu_item_id
            AND EXISTS (
                SELECT owner_1.id
                FROM recipeweave.menu AS owner_1
                WHERE
                    owner_1.id = owner_0.menu_id
                    AND owner_1.user_id = %(actor_id)s
            )
    ))) AS rows_menu_ingredient_override,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'user_id', t.user_id,
                'resource_type_id', t.resource_type_id,
                'name', t.name,
                'capacity', t.capacity::TEXT,
                'quantity', t.quantity,
                'active', t.active
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.kitchen_resource AS t
        WHERE (t.user_id = %(actor_id)s)
    ) AS rows_kitchen_resource,
    (SELECT
        COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
            'id', t.id,
            'created_at', t.created_at,
            'menu_id', t.menu_id,
            'menu_revision', t.menu_revision,
            'status', t.status,
            'target_at', t.target_at,
            'planner_version', t.planner_version,
            'input_snapshot', t.input_snapshot,
            'input_hash', t.input_hash,
            'current_task_index', t.current_task_index
        ) ORDER BY t.id), '[]'::JSONB)
    FROM recipeweave.cooking_session AS t
    WHERE (EXISTS (
        SELECT owner_0.id
        FROM recipeweave.menu AS owner_0
        WHERE
            owner_0.id = t.menu_id
            AND owner_0.user_id = %(actor_id)s
    ))) AS rows_cooking_session,
    (SELECT
        COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
            'id', t.id,
            'created_at', t.created_at,
            'session_id', t.session_id,
            'menu_item_id', t.menu_item_id,
            'step_id', t.step_id,
            'batch_no', t.batch_no,
            'planned_start_s', t.planned_start_s,
            'planned_end_s', t.planned_end_s,
            'status', t.status,
            'actual_start_at', t.actual_start_at,
            'actual_end_at', t.actual_end_at,
            'timer_started_at', t.timer_started_at,
            'timer_duration_s', t.timer_duration_s,
            'duration_source', t.duration_source,
            'confirmed_duration_s', t.confirmed_duration_s
        ) ORDER BY t.id), '[]'::JSONB)
    FROM recipeweave.session_task AS t
    WHERE (EXISTS (
        SELECT owner_0.id
        FROM recipeweave.cooking_session AS owner_0
        WHERE
            owner_0.id = t.session_id
            AND EXISTS (
                SELECT owner_1.id
                FROM recipeweave.menu AS owner_1
                WHERE
                    owner_1.id = owner_0.menu_id
                    AND owner_1.user_id = %(actor_id)s
            )
    ))) AS rows_session_task,
    (SELECT
        COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
            'id', t.id,
            'created_at', t.created_at,
            'before_task_id', t.before_task_id,
            'after_task_id', t.after_task_id,
            'min_lag_s', t.min_lag_s,
            'max_lag_s', t.max_lag_s,
            'reason', t.reason
        ) ORDER BY t.id), '[]'::JSONB)
    FROM recipeweave.task_dependency AS t
    WHERE (EXISTS (
        SELECT owner_0.id
        FROM recipeweave.session_task AS owner_0
        WHERE
            owner_0.id = t.before_task_id
            AND EXISTS (
                SELECT owner_1.id
                FROM recipeweave.cooking_session AS owner_1
                WHERE
                    owner_1.id = owner_0.session_id
                    AND EXISTS (
                        SELECT owner_2.id
                        FROM recipeweave.menu AS owner_2
                        WHERE
                            owner_2.id = owner_1.menu_id
                            AND owner_2.user_id = %(actor_id)s
                    )
            )
    ))) AS rows_task_dependency,
    (SELECT
        COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
            'id', t.id,
            'created_at', t.created_at,
            'task_id', t.task_id,
            'resource_id', t.resource_id,
            'start_s', t.start_s,
            'end_s', t.end_s,
            'quantity', t.quantity
        ) ORDER BY t.id), '[]'::JSONB)
    FROM recipeweave.resource_reservation AS t
    WHERE (EXISTS (
        SELECT owner_0.id
        FROM recipeweave.session_task AS owner_0
        WHERE
            owner_0.id = t.task_id
            AND EXISTS (
                SELECT owner_1.id
                FROM recipeweave.cooking_session AS owner_1
                WHERE
                    owner_1.id = owner_0.session_id
                    AND EXISTS (
                        SELECT owner_2.id
                        FROM recipeweave.menu AS owner_2
                        WHERE
                            owner_2.id = owner_1.menu_id
                            AND owner_2.user_id = %(actor_id)s
                    )
            )
    ))) AS rows_resource_reservation,
    (SELECT
        COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
            'id', t.id,
            'created_at', t.created_at,
            'session_id', t.session_id,
            'form_id', t.form_id,
            'product_version_id', t.product_version_id,
            'unit_id', t.unit_id,
            'required_amount', t.required_amount::TEXT,
            'quality', t.quality,
            'calculation_version', t.calculation_version,
            'actual_amount', t.actual_amount::TEXT,
            'consumption_outcome', t.consumption_outcome
        ) ORDER BY t.id), '[]'::JSONB)
    FROM recipeweave.ingredient_total AS t
    WHERE (EXISTS (
        SELECT owner_0.id
        FROM recipeweave.cooking_session AS owner_0
        WHERE
            owner_0.id = t.session_id
            AND EXISTS (
                SELECT owner_1.id
                FROM recipeweave.menu AS owner_1
                WHERE
                    owner_1.id = owner_0.menu_id
                    AND owner_1.user_id = %(actor_id)s
            )
    ))) AS rows_ingredient_total,
    (SELECT
        COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
            'id', t.id,
            'created_at', t.created_at,
            'user_id', t.user_id,
            'form_id', t.form_id,
            'product_version_id', t.product_version_id,
            'amount', t.amount::TEXT,
            'unit_id', t.unit_id,
            'expires_on', t.expires_on,
            'opened_at', t.opened_at,
            'location', t.location,
            'priority', t.priority,
            'status', t.status,
            'source_import_id', t.source_import_id,
            'quantity_quality', t.quantity_quality,
            'original_form_id', t.original_form_id,
            'original_amount', t.original_amount::TEXT,
            'original_unit_id', t.original_unit_id,
            'updated_at', t.updated_at,
            'edited', t.edited
        ) ORDER BY t.id), '[]'::JSONB)
    FROM recipeweave.pantry_lot AS t
    WHERE (t.user_id = %(actor_id)s)) AS rows_pantry_lot,
    (SELECT
        COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
            'id', t.id,
            'created_at', t.created_at,
            'session_id', t.session_id,
            'total_id', t.total_id,
            'product_version_id', t.product_version_id,
            'net_shortage', t.net_shortage::TEXT,
            'package_count', t.package_count,
            'surplus_amount', t.surplus_amount::TEXT,
            'checked', t.checked,
            'client_key', t.client_key,
            'checked_at', t.checked_at,
            'archived', t.archived
        ) ORDER BY t.id), '[]'::JSONB)
    FROM recipeweave.shopping_item AS t
    WHERE (EXISTS (
        SELECT owner_0.id
        FROM recipeweave.cooking_session AS owner_0
        WHERE
            owner_0.id = t.session_id
            AND EXISTS (
                SELECT owner_1.id
                FROM recipeweave.menu AS owner_1
                WHERE
                    owner_1.id = owner_0.menu_id
                    AND owner_1.user_id = %(actor_id)s
            )
    ))) AS rows_shopping_item,
    (SELECT
        COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
            'id', t.id,
            'created_at', t.created_at,
            'user_id', t.user_id,
            'file_sha256', t.file_sha256,
            'idempotency_key', t.idempotency_key,
            'status', t.status,
            'revision', t.revision::TEXT,
            'committed_at', t.committed_at,
            'reverted_at', t.reverted_at,
            'undo_preserved_count', t.undo_preserved_count
        ) ORDER BY t.id), '[]'::JSONB)
    FROM recipeweave.receipt_import AS t
    WHERE (t.user_id = %(actor_id)s)) AS rows_receipt_import,
    (SELECT
        COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
            'id', t.id,
            'created_at', t.created_at,
            'import_id', t.import_id,
            'line_no', t.line_no,
            'raw_name', t.raw_name,
            'form_id', t.form_id,
            'product_version_id', t.product_version_id,
            'amount', t.amount::TEXT,
            'unit_id', t.unit_id,
            'decision', t.decision,
            'pantry_lot_id', t.pantry_lot_id
        ) ORDER BY t.id), '[]'::JSONB)
    FROM recipeweave.receipt_line AS t
    WHERE (EXISTS (
        SELECT owner_0.id
        FROM recipeweave.receipt_import AS owner_0
        WHERE
            owner_0.id = t.import_id
            AND owner_0.user_id = %(actor_id)s
    ))) AS rows_receipt_line,
    (SELECT
        COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
            'id', t.id,
            'created_at', t.created_at,
            'user_id', t.user_id,
            'food_id', t.food_id
        ) ORDER BY t.id), '[]'::JSONB)
    FROM recipeweave.user_food AS t
    WHERE (t.user_id = %(actor_id)s)) AS rows_user_food,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'user_id', t.user_id,
                'food_id', t.food_id
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.user_pantry_food AS t
        WHERE (t.user_id = %(actor_id)s)
    ) AS rows_user_pantry_food,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'user_id', t.user_id,
                'session_id', t.session_id,
                'lot_id', t.lot_id,
                'amount', t.amount::TEXT,
                'unit_id', t.unit_id
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.pantry_consumption AS t
        WHERE (t.user_id = %(actor_id)s)
    ) AS rows_pantry_consumption,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'user_id', t.user_id,
                'key', t.key,
                'signature', t.signature,
                'food_id', t.food_id,
                'amount', t.amount::TEXT,
                'unit_id', t.unit_id,
                'checked_at', t.checked_at,
                'archived', t.archived
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.user_shopping_check AS t
        WHERE (t.user_id = %(actor_id)s)
    ) AS rows_user_shopping_check,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'version', t.version,
                'manifest_hash', t.manifest_hash,
                'published_at', t.published_at,
                'owner_id', t.owner_id
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.catalog_release AS t
        WHERE (t.owner_id = %(actor_id)s)
    ) AS rows_catalog_release,
    (SELECT
        COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
            'id', t.id,
            'created_at', t.created_at,
            'code', t.code,
            'name', t.name,
            'kind', t.kind,
            'parent_id', t.parent_id,
            'release_id', t.release_id,
            'status', t.status,
            'owner_id', t.owner_id
        ) ORDER BY t.id), '[]'::JSONB)
    FROM recipeweave.food AS t
    WHERE (t.owner_id = %(actor_id)s)) AS rows_food,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'food_id', t.food_id,
                'alias', t.alias,
                'locale', t.locale
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.food_alias AS t
        WHERE (EXISTS (
            SELECT 1 FROM recipeweave.food AS food
            WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s
        ))
    ) AS rows_food_alias,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'food_id', t.food_id,
                'name', t.name,
                'state', t.state,
                'base_unit_id', t.base_unit_id,
                'quantity_basis', t.quantity_basis,
                'status', t.status
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.food_form AS t
        WHERE (EXISTS (
            SELECT 1 FROM recipeweave.food AS food
            WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s
        ))
    ) AS rows_food_form,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'food_id', t.food_id,
                'option_id', t.option_id
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.food_axis_option AS t
        WHERE (EXISTS (
            SELECT 1 FROM recipeweave.food AS food
            WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s
        ))
    ) AS rows_food_axis_option,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'food_id', t.food_id,
                'brand', t.brand,
                'name', t.name,
                'gtin', t.gtin,
                'status', t.status
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.product AS t
        WHERE (EXISTS (
            SELECT 1 FROM recipeweave.food AS food
            WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s
        ))
    ) AS rows_product,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'form_id', t.form_id,
                'from_unit_id', t.from_unit_id,
                'to_unit_id', t.to_unit_id,
                'factor', t.factor::TEXT,
                'quality', t.quality,
                'source_id', t.source_id,
                'conditions', t.conditions,
                'release_id', t.release_id
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.conversion AS t
        WHERE
            (EXISTS (
                SELECT 1
                FROM recipeweave.food AS food
                INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id
                WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s
            ))
    ) AS rows_conversion,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'form_id', t.form_id,
                'allergen_id', t.allergen_id,
                'presence', t.presence,
                'source_id', t.source_id
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.food_allergen AS t
        WHERE
            (EXISTS (
                SELECT 1
                FROM recipeweave.food AS food
                INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id
                WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s
            ))
    ) AS rows_food_allergen,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'product_id', t.product_id,
                'version', t.version,
                'form_id', t.form_id,
                'net_amount', t.net_amount::TEXT,
                'unit_id', t.unit_id,
                'drain_amount', t.drain_amount::TEXT,
                'source_id', t.source_id,
                'preparation_note', t.preparation_note,
                'valid_from', t.valid_from
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.product_version AS t
        WHERE
            (EXISTS (
                SELECT 1
                FROM recipeweave.food AS food
                INNER JOIN recipeweave.product AS product ON food.id = product.food_id
                WHERE product.id = t.product_id AND food.owner_id = %(actor_id)s
            ))
    ) AS rows_product_version,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'product_version_id', t.product_version_id,
                'form_id', t.form_id,
                'name', t.name,
                'amount', t.amount::TEXT,
                'unit_id', t.unit_id,
                'quality', t.quality
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.product_component AS t
        WHERE
            (EXISTS (
                SELECT 1
                FROM recipeweave.food AS food
                INNER JOIN recipeweave.product AS product ON food.id = product.food_id
                INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id
                WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s
            ))
    ) AS rows_product_component,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'product_version_id', t.product_version_id,
                'allergen_id', t.allergen_id,
                'presence', t.presence,
                'source_id', t.source_id
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.product_allergen AS t
        WHERE
            (EXISTS (
                SELECT 1
                FROM recipeweave.food AS food
                INNER JOIN recipeweave.product AS product ON food.id = product.food_id
                INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id
                WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s
            ))
    ) AS rows_product_allergen,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'product_version_id', t.product_version_id,
                'operation_id', t.operation_id,
                'allowed', t.allowed,
                'use_original_container', t.use_original_container,
                'parameter_contract', t.parameter_contract,
                'source_id', t.source_id
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.product_preparation_rule AS t
        WHERE
            (EXISTS (
                SELECT 1
                FROM recipeweave.food AS food
                INNER JOIN recipeweave.product AS product ON food.id = product.food_id
                INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id
                WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s
            ))
    ) AS rows_product_preparation_rule,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'form_id', t.form_id,
                'product_version_id', t.product_version_id,
                'nutrient_id', t.nutrient_id,
                'amount', t.amount::TEXT,
                'basis_amount', t.basis_amount::TEXT,
                'basis_unit_id', t.basis_unit_id,
                'source_id', t.source_id
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.nutrition_fact AS t
        WHERE
            (
                EXISTS (
                    SELECT 1
                    FROM recipeweave.food AS food
                    INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id
                    WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s
                )
                OR EXISTS (
                    SELECT 1
                    FROM recipeweave.food AS food
                    INNER JOIN recipeweave.product AS product ON food.id = product.food_id
                    INNER JOIN
                        recipeweave.product_version AS version
                        ON product.id = version.product_id
                    WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s
                )
            )
    ) AS rows_nutrition_fact,
    (
        SELECT
            COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT(
                'id', t.id,
                'created_at', t.created_at,
                'input_form_id', t.input_form_id,
                'output_form_id', t.output_form_id,
                'yield_ratio', t.yield_ratio::TEXT,
                'source_id', t.source_id,
                'quality', t.quality,
                'conditions', t.conditions
            ) ORDER BY t.id), '[]'::JSONB)
        FROM recipeweave.form_yield AS t
        WHERE
            (EXISTS (
                SELECT 1
                FROM recipeweave.food AS food
                INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id
                WHERE form.id = t.input_form_id AND food.owner_id = %(actor_id)s
            ))
    ) AS rows_form_yield;
```

## backend/src/app/apis/backup/export_backup/sql/q021_issue_artifact.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.backup_artifact | C | body_sha256, format_version, id, user_id |

バインド変数: actor_id, artifact_id, body_sha256

```sql
-- バックアップ本文を保存せず、本人への発行根拠だけを記録する。
INSERT INTO recipeweave.backup_artifact (id, user_id, body_sha256, format_version)
VALUES (%(artifact_id)s, %(actor_id)s, %(body_sha256)s, 2);
```

## backend/src/app/apis/auth/get_me/sql/q001_set_identity.sql

実行条件: 認証依存の初期化時。同一主体の初回INSERTのみ作成し、既存行はDO NOTHING。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|

バインド変数: role, user_id

```sql
-- 検証済み主体を、この要求のトランザクションにだけ適用する。
SELECT
    SET_CONFIG('recipeweave.user_id', %(user_id)s, TRUE) AS user_setting,
    SET_CONFIG('recipeweave.role', %(role)s, TRUE) AS role_setting;
```

## backend/src/app/apis/auth/get_me/sql/q002_initialize_user.sql

実行条件: 認証依存の初期化時。同一主体の初回INSERTのみ作成し、既存行はDO NOTHING。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.app_user | C | auth_subject, id, locale, state, timezone |

バインド変数: subject, user_id

```sql
-- 認証主体から決定的に採番した本人行を初回だけ作る。
INSERT INTO recipeweave.app_user (id, auth_subject, state, locale, timezone)
VALUES (%(user_id)s, %(subject)s, 'active', 'ja', 'Asia/Tokyo')
ON CONFLICT (auth_subject) DO NOTHING
RETURNING id;
```

## backend/src/app/apis/auth/get_me/sql/q003_select_user.sql

実行条件: 認証依存の初期化時。同一主体の初回INSERTのみ作成し、既存行はDO NOTHING。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.app_user | R | auth_subject, id, state |

バインド変数: subject, user_id

```sql
-- 主体とIDが両方一致する有効状態を確認する。
SELECT
    id,
    state
FROM recipeweave.app_user
WHERE id = %(user_id)s AND auth_subject = %(subject)s;
```

## backend/src/app/apis/auth/get_me/sql/q004_initialize_revision.sql

実行条件: 認証依存の初期化時。同一主体の初回INSERTのみ作成し、既存行はDO NOTHING。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.workspace_revision | C | id, revision, user_id |

バインド変数: row_id, user_id

```sql
-- 初回のみ版を初期化し、ログインで既存版を変更しない。
INSERT INTO recipeweave.workspace_revision (id, user_id, revision)
VALUES (%(row_id)s, %(user_id)s, 0) ON CONFLICT (user_id) DO NOTHING;
```

## backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql

実行条件: 認証依存の初期化時。同一主体の初回INSERTのみ作成し、既存行はDO NOTHING。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.kitchen_resource | C,R | active, capacity, id, name, quantity, resource_type_id, user_id |
| recipeweave.resource_type | R | code, id, name, status |

バインド変数: resource_code, row_id, user_id

```sql
-- 初回ログイン時の作業枠だけを作り、利用者が選ぶ可視器具は追加しない。
INSERT INTO recipeweave.kitchen_resource (
    id, user_id, resource_type_id, name, capacity, quantity, active
)
SELECT
    %(row_id)s AS id,
    %(user_id)s AS user_id,
    resource_kind.id AS resource_type_id,
    resource_kind.name,
    NULL AS capacity,
    1 AS quantity,
    TRUE AS active
FROM recipeweave.resource_type AS resource_kind
WHERE
    resource_kind.code = %(resource_code)s
    AND resource_kind.code IN ('person', 'burner', 'bowl')
    AND resource_kind.status = 'active'
    AND NOT EXISTS (
        SELECT 1 FROM recipeweave.kitchen_resource AS kitchen
        WHERE kitchen.user_id = %(user_id)s AND kitchen.resource_type_id = resource_kind.id
    )
ON CONFLICT (id) DO NOTHING
RETURNING id;
```

SQLファイル→自動生成wrapper→連携adapter→functions→routerの境界で管理する。利用者入力はパラメーターとして渡し、SQL文字列へ連結しない。
