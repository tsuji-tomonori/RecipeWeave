# SQL仕様: preview_backup

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## backend/src/app/apis/backup/preview_backup/sql/q001_lock_revision.sql

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

## backend/src/app/apis/backup/preview_backup/sql/q002_profile.sql

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

## backend/src/app/apis/backup/preview_backup/sql/q010_export_tables.sql

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

## backend/src/app/apis/backup/preview_backup/sql/q020_artifact.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.backup_artifact | R | body_sha256, format_version, id, user_id |

バインド変数: actor_id, artifact_id, body_sha256

```sql
-- 発行した本人と本文digestが一致する根拠だけを認可に使う。
SELECT id FROM recipeweave.backup_artifact
WHERE
    id = %(artifact_id)s AND user_id = %(actor_id)s
    AND body_sha256 = %(body_sha256)s AND format_version = 2;
```

## backend/src/app/apis/backup/preview_backup/sql/q022_issue_intent.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.backup_restore_intent | C | artifact_id, body_sha256, current_revision, expires_at, id, user_id |

バインド変数: actor_id, artifact_id, body_sha256, current_revision, intent_id

```sql
-- 検証した本文と現在版を15分間の最終確認へ結び付ける。
INSERT INTO recipeweave.backup_restore_intent
(id, user_id, artifact_id, body_sha256, current_revision, expires_at)
VALUES (
    %(intent_id)s, %(actor_id)s, %(artifact_id)s, %(body_sha256)s,
    %(current_revision)s, CURRENT_TIMESTAMP + INTERVAL '15 minutes'
)
RETURNING id, expires_at;
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_catalog_release.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.catalog_release | D | owner_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人のカタログ公開版だけを削除する。
DELETE FROM recipeweave.catalog_release AS t
WHERE (t.owner_id = %(actor_id)s);
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_conversion.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.conversion | D | form_id |
| recipeweave.food | R | id, owner_id |
| recipeweave.food_form | R | food_id, id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の食材形態別換算だけを削除する。
DELETE FROM recipeweave.conversion AS t
WHERE
    (EXISTS (
        SELECT 1
        FROM recipeweave.food AS food
        INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id
        WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s
    ));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_cooking_session.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.cooking_session | D | menu_id |
| recipeweave.menu | R | id, user_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の調理計画実行だけを削除する。
DELETE FROM recipeweave.cooking_session AS t
WHERE (EXISTS (
    SELECT owner_0.id
    FROM recipeweave.menu AS owner_0
    WHERE
        owner_0.id = t.menu_id
        AND owner_0.user_id = %(actor_id)s
));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_food.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | D | owner_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の購入・利用食材概念だけを削除する。
DELETE FROM recipeweave.food AS t
WHERE (t.owner_id = %(actor_id)s);
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_food_alias.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | R | id, owner_id |
| recipeweave.food_alias | D | food_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の食材別名だけを削除する。
DELETE FROM recipeweave.food_alias AS t
WHERE (EXISTS (
    SELECT 1 FROM recipeweave.food AS food
    WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s
));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_food_allergen.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | R | id, owner_id |
| recipeweave.food_allergen | D | form_id |
| recipeweave.food_form | R | food_id, id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の食材アレルゲン知識だけを削除する。
DELETE FROM recipeweave.food_allergen AS t
WHERE
    (EXISTS (
        SELECT 1
        FROM recipeweave.food AS food
        INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id
        WHERE form.id = t.form_id AND food.owner_id = %(actor_id)s
    ));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_food_axis_option.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | R | id, owner_id |
| recipeweave.food_axis_option | D | food_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の食材の分類属性だけを削除する。
DELETE FROM recipeweave.food_axis_option AS t
WHERE (EXISTS (
    SELECT 1 FROM recipeweave.food AS food
    WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s
));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_food_form.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | R | id, owner_id |
| recipeweave.food_form | D | food_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の食材形態だけを削除する。
DELETE FROM recipeweave.food_form AS t
WHERE (EXISTS (
    SELECT 1 FROM recipeweave.food AS food
    WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s
));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_form_yield.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | R | id, owner_id |
| recipeweave.food_form | R | food_id, id |
| recipeweave.form_yield | D | input_form_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の処理歩留まりだけを削除する。
DELETE FROM recipeweave.form_yield AS t
WHERE
    (EXISTS (
        SELECT 1
        FROM recipeweave.food AS food
        INNER JOIN recipeweave.food_form AS form ON food.id = form.food_id
        WHERE form.id = t.input_form_id AND food.owner_id = %(actor_id)s
    ));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_ingredient_total.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.cooking_session | R | id, menu_id |
| recipeweave.ingredient_total | D | session_id |
| recipeweave.menu | R | id, user_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の献立材料集計結果だけを削除する。
DELETE FROM recipeweave.ingredient_total AS t
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
));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_kitchen_resource.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.kitchen_resource | D | user_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人のキッチンの実資源だけを削除する。
DELETE FROM recipeweave.kitchen_resource AS t
WHERE (t.user_id = %(actor_id)s);
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_menu.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.menu | D | user_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の献立だけを削除する。
DELETE FROM recipeweave.menu AS t
WHERE (t.user_id = %(actor_id)s);
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_menu_ingredient_override.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.menu | R | id, user_id |
| recipeweave.menu_ingredient_override | D | menu_item_id |
| recipeweave.menu_item | R | id, menu_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の献立別材料確定だけを削除する。
DELETE FROM recipeweave.menu_ingredient_override AS t
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
));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_menu_item.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.menu | R | id, user_id |
| recipeweave.menu_item | D | menu_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の献立の料理だけを削除する。
DELETE FROM recipeweave.menu_item AS t
WHERE (EXISTS (
    SELECT owner_0.id
    FROM recipeweave.menu AS owner_0
    WHERE
        owner_0.id = t.menu_id
        AND owner_0.user_id = %(actor_id)s
));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_nutrition_fact.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | R | id, owner_id |
| recipeweave.food_form | R | food_id, id |
| recipeweave.nutrition_fact | D | form_id, product_version_id |
| recipeweave.product | R | food_id, id |
| recipeweave.product_version | R | id, product_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の形態・商品別栄養値だけを削除する。
DELETE FROM recipeweave.nutrition_fact AS t
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
            INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id
            WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s
        )
    );
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_pantry_consumption.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.pantry_consumption | D | user_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の調理による在庫消費の冪等台帳だけを削除する。
DELETE FROM recipeweave.pantry_consumption AS t
WHERE (t.user_id = %(actor_id)s);
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_pantry_lot.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.pantry_lot | D | user_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の手持ち食材ロットだけを削除する。
DELETE FROM recipeweave.pantry_lot AS t
WHERE (t.user_id = %(actor_id)s);
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_product.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | R | id, owner_id |
| recipeweave.product | D | food_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の市販商品識別だけを削除する。
DELETE FROM recipeweave.product AS t
WHERE (EXISTS (
    SELECT 1 FROM recipeweave.food AS food
    WHERE food.id = t.food_id AND food.owner_id = %(actor_id)s
));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_product_allergen.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | R | id, owner_id |
| recipeweave.product | R | food_id, id |
| recipeweave.product_allergen | D | product_version_id |
| recipeweave.product_version | R | id, product_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の商品表示アレルゲンだけを削除する。
DELETE FROM recipeweave.product_allergen AS t
WHERE
    (EXISTS (
        SELECT 1
        FROM recipeweave.food AS food
        INNER JOIN recipeweave.product AS product ON food.id = product.food_id
        INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id
        WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s
    ));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_product_component.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | R | id, owner_id |
| recipeweave.product | R | food_id, id |
| recipeweave.product_component | D | product_version_id |
| recipeweave.product_version | R | id, product_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人のセット内構成品だけを削除する。
DELETE FROM recipeweave.product_component AS t
WHERE
    (EXISTS (
        SELECT 1
        FROM recipeweave.food AS food
        INNER JOIN recipeweave.product AS product ON food.id = product.food_id
        INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id
        WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s
    ));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_product_preparation_rule.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | R | id, owner_id |
| recipeweave.product | R | food_id, id |
| recipeweave.product_preparation_rule | D | product_version_id |
| recipeweave.product_version | R | id, product_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の商品固有の調理条件だけを削除する。
DELETE FROM recipeweave.product_preparation_rule AS t
WHERE
    (EXISTS (
        SELECT 1
        FROM recipeweave.food AS food
        INNER JOIN recipeweave.product AS product ON food.id = product.food_id
        INNER JOIN recipeweave.product_version AS version ON product.id = version.product_id
        WHERE version.id = t.product_version_id AND food.owner_id = %(actor_id)s
    ));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_product_version.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | R | id, owner_id |
| recipeweave.product | R | food_id, id |
| recipeweave.product_version | D | product_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の商品仕様版だけを削除する。
DELETE FROM recipeweave.product_version AS t
WHERE
    (EXISTS (
        SELECT 1
        FROM recipeweave.food AS food
        INNER JOIN recipeweave.product AS product ON food.id = product.food_id
        WHERE product.id = t.product_id AND food.owner_id = %(actor_id)s
    ));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_receipt_import.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.receipt_import | D | user_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人のレシート読取・在庫登録の処理単位だけを削除する。
DELETE FROM recipeweave.receipt_import AS t
WHERE (t.user_id = %(actor_id)s);
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_receipt_line.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.receipt_import | R | id, user_id |
| recipeweave.receipt_line | D | import_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人のレシートの商品候補と確定した在庫の対応だけを削除する。
DELETE FROM recipeweave.receipt_line AS t
WHERE (EXISTS (
    SELECT owner_0.id
    FROM recipeweave.receipt_import AS owner_0
    WHERE
        owner_0.id = t.import_id
        AND owner_0.user_id = %(actor_id)s
));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_resource_reservation.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.cooking_session | R | id, menu_id |
| recipeweave.menu | R | id, user_id |
| recipeweave.resource_reservation | D | task_id |
| recipeweave.session_task | R | id, session_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の資源の予約だけを削除する。
DELETE FROM recipeweave.resource_reservation AS t
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
));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_session_task.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.cooking_session | R | id, menu_id |
| recipeweave.menu | R | id, user_id |
| recipeweave.session_task | D | session_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の展開済み工程だけを削除する。
DELETE FROM recipeweave.session_task AS t
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
));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_shopping_item.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.cooking_session | R | id, menu_id |
| recipeweave.menu | R | id, user_id |
| recipeweave.shopping_item | D | session_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の買い物行だけを削除する。
DELETE FROM recipeweave.shopping_item AS t
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
));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_task_dependency.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.cooking_session | R | id, menu_id |
| recipeweave.menu | R | id, user_id |
| recipeweave.session_task | R | id, session_id |
| recipeweave.task_dependency | D | before_task_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の献立展開後依存だけを削除する。
DELETE FROM recipeweave.task_dependency AS t
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
));
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_user_exclusion.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.user_exclusion | D | user_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の避けたい食材・物質だけを削除する。
DELETE FROM recipeweave.user_exclusion AS t
WHERE (t.user_id = %(actor_id)s);
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_user_food.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.user_food | D | user_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の利用者が追加した独自食材の所有だけを削除する。
DELETE FROM recipeweave.user_food AS t
WHERE (t.user_id = %(actor_id)s);
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_user_pantry_food.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.user_pantry_food | D | user_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の利用者が常備すると設定した食材だけを削除する。
DELETE FROM recipeweave.user_pantry_food AS t
WHERE (t.user_id = %(actor_id)s);
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_user_preference.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.user_preference | D | user_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人のユーザーの嗜好だけを削除する。
DELETE FROM recipeweave.user_preference AS t
WHERE (t.user_id = %(actor_id)s);
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_user_recipe_event.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.user_recipe_event | D | user_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の提案・調理履歴だけを削除する。
DELETE FROM recipeweave.user_recipe_event AS t
WHERE (t.user_id = %(actor_id)s);
```

## backend/src/app/apis/backup/preview_backup/sql/q100_delete_user_shopping_check.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.user_shopping_check | D | user_id |

バインド変数: actor_id

```sql
-- 全置換の確認対象である本人の調理前の買い物確認だけを削除する。
DELETE FROM recipeweave.user_shopping_check AS t
WHERE (t.user_id = %(actor_id)s);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_catalog_release.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.catalog_release | C | created_at, id, manifest_hash, owner_id, published_at, version |

バインド変数: created_at, id, manifest_hash, owner_id, published_at, version

```sql
-- 検証済みバックアップのカタログ公開版を元IDと全列で復元する。
INSERT INTO recipeweave.catalog_release (
    id,
    created_at,
    version,
    manifest_hash,
    published_at,
    owner_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(version)s,
    %(manifest_hash)s,
    %(published_at)s,
    %(owner_id)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_conversion.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.conversion | C | conditions, created_at, factor, form_id, from_unit_id, id, quality, release_id, source_id, to_unit_id |

バインド変数: conditions, created_at, factor, form_id, from_unit_id, id, quality, release_id, source_id, to_unit_id

```sql
-- 検証済みバックアップの食材形態別換算を元IDと全列で復元する。
INSERT INTO recipeweave.conversion (
    id,
    created_at,
    form_id,
    from_unit_id,
    to_unit_id,
    factor,
    quality,
    source_id,
    conditions,
    release_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(form_id)s,
    %(from_unit_id)s,
    %(to_unit_id)s,
    %(factor)s,
    %(quality)s,
    %(source_id)s,
    %(conditions)s,
    %(release_id)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_cooking_session.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.cooking_session | C | created_at, current_task_index, id, input_hash, input_snapshot, menu_id, menu_revision, planner_version, status, target_at |

バインド変数: created_at, current_task_index, id, input_hash, input_snapshot, menu_id, menu_revision, planner_version, status, target_at

```sql
-- 検証済みバックアップの調理計画実行を元IDと全列で復元する。
INSERT INTO recipeweave.cooking_session (
    id,
    created_at,
    menu_id,
    menu_revision,
    status,
    target_at,
    planner_version,
    input_snapshot,
    input_hash,
    current_task_index
) VALUES (
    %(id)s,
    %(created_at)s,
    %(menu_id)s,
    %(menu_revision)s,
    %(status)s,
    %(target_at)s,
    %(planner_version)s,
    %(input_snapshot)s,
    %(input_hash)s,
    %(current_task_index)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_food.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | C | code, created_at, id, kind, name, owner_id, parent_id, release_id, status |

バインド変数: code, created_at, id, kind, name, owner_id, parent_id, release_id, status

```sql
-- 検証済みバックアップの購入・利用食材概念を元IDと全列で復元する。
INSERT INTO recipeweave.food (
    id,
    created_at,
    code,
    name,
    kind,
    parent_id,
    release_id,
    status,
    owner_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(code)s,
    %(name)s,
    %(kind)s,
    %(parent_id)s,
    %(release_id)s,
    %(status)s,
    %(owner_id)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_food_alias.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food_alias | C | alias, created_at, food_id, id, locale |

バインド変数: alias, created_at, food_id, id, locale

```sql
-- 検証済みバックアップの食材別名を元IDと全列で復元する。
INSERT INTO recipeweave.food_alias (
    id,
    created_at,
    food_id,
    alias,
    locale
) VALUES (
    %(id)s,
    %(created_at)s,
    %(food_id)s,
    %(alias)s,
    %(locale)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_food_allergen.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food_allergen | C | allergen_id, created_at, form_id, id, presence, source_id |

バインド変数: allergen_id, created_at, form_id, id, presence, source_id

```sql
-- 検証済みバックアップの食材アレルゲン知識を元IDと全列で復元する。
INSERT INTO recipeweave.food_allergen (
    id,
    created_at,
    form_id,
    allergen_id,
    presence,
    source_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(form_id)s,
    %(allergen_id)s,
    %(presence)s,
    %(source_id)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_food_axis_option.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food_axis_option | C | created_at, food_id, id, option_id |

バインド変数: created_at, food_id, id, option_id

```sql
-- 検証済みバックアップの食材の分類属性を元IDと全列で復元する。
INSERT INTO recipeweave.food_axis_option (
    id,
    created_at,
    food_id,
    option_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(food_id)s,
    %(option_id)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_food_form.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food_form | C | base_unit_id, created_at, food_id, id, name, quantity_basis, state, status |

バインド変数: base_unit_id, created_at, food_id, id, name, quantity_basis, state, status

```sql
-- 検証済みバックアップの食材形態を元IDと全列で復元する。
INSERT INTO recipeweave.food_form (
    id,
    created_at,
    food_id,
    name,
    state,
    base_unit_id,
    quantity_basis,
    status
) VALUES (
    %(id)s,
    %(created_at)s,
    %(food_id)s,
    %(name)s,
    %(state)s,
    %(base_unit_id)s,
    %(quantity_basis)s,
    %(status)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_form_yield.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.form_yield | C | conditions, created_at, id, input_form_id, output_form_id, quality, source_id, yield_ratio |

バインド変数: conditions, created_at, id, input_form_id, output_form_id, quality, source_id, yield_ratio

```sql
-- 検証済みバックアップの処理歩留まりを元IDと全列で復元する。
INSERT INTO recipeweave.form_yield (
    id,
    created_at,
    input_form_id,
    output_form_id,
    yield_ratio,
    source_id,
    quality,
    conditions
) VALUES (
    %(id)s,
    %(created_at)s,
    %(input_form_id)s,
    %(output_form_id)s,
    %(yield_ratio)s,
    %(source_id)s,
    %(quality)s,
    %(conditions)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_ingredient_total.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.ingredient_total | C | actual_amount, calculation_version, consumption_outcome, created_at, form_id, id, product_version_id, quality, required_amount, session_id, unit_id |

バインド変数: actual_amount, calculation_version, consumption_outcome, created_at, form_id, id, product_version_id, quality, required_amount, session_id, unit_id

```sql
-- 検証済みバックアップの献立材料集計結果を元IDと全列で復元する。
INSERT INTO recipeweave.ingredient_total (
    id,
    created_at,
    session_id,
    form_id,
    product_version_id,
    unit_id,
    required_amount,
    quality,
    calculation_version,
    actual_amount,
    consumption_outcome
) VALUES (
    %(id)s,
    %(created_at)s,
    %(session_id)s,
    %(form_id)s,
    %(product_version_id)s,
    %(unit_id)s,
    %(required_amount)s,
    %(quality)s,
    %(calculation_version)s,
    %(actual_amount)s,
    %(consumption_outcome)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_kitchen_resource.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.kitchen_resource | C | active, capacity, created_at, id, name, quantity, resource_type_id, user_id |

バインド変数: active, capacity, created_at, id, name, quantity, resource_type_id, user_id

```sql
-- 検証済みバックアップのキッチンの実資源を元IDと全列で復元する。
INSERT INTO recipeweave.kitchen_resource (
    id,
    created_at,
    user_id,
    resource_type_id,
    name,
    capacity,
    quantity,
    active
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(resource_type_id)s,
    %(name)s,
    %(capacity)s,
    %(quantity)s,
    %(active)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_menu.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.menu | C | created_at, id, name, revision, servings, user_id |

バインド変数: created_at, id, name, revision, servings, user_id

```sql
-- 検証済みバックアップの献立を元IDと全列で復元する。
INSERT INTO recipeweave.menu (
    id,
    created_at,
    user_id,
    name,
    servings,
    revision
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(name)s,
    %(servings)s,
    %(revision)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_menu_ingredient_override.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.menu_ingredient_override | C | amount, created_at, form_id, id, ingredient_line_id, menu_item_id, product_version_id, selected |

バインド変数: amount, created_at, form_id, id, ingredient_line_id, menu_item_id, product_version_id, selected

```sql
-- 検証済みバックアップの献立別材料確定を元IDと全列で復元する。
INSERT INTO recipeweave.menu_ingredient_override (
    id,
    created_at,
    menu_item_id,
    ingredient_line_id,
    selected,
    amount,
    form_id,
    product_version_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(menu_item_id)s,
    %(ingredient_line_id)s,
    %(selected)s,
    %(amount)s,
    %(form_id)s,
    %(product_version_id)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_menu_item.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.menu_item | C | created_at, id, menu_id, position, recipe_version_id, role_option_id, servings |

バインド変数: created_at, id, menu_id, position, recipe_version_id, role_option_id, servings

```sql
-- 検証済みバックアップの献立の料理を元IDと全列で復元する。
INSERT INTO recipeweave.menu_item (
    id,
    created_at,
    menu_id,
    recipe_version_id,
    servings,
    role_option_id,
    position
) VALUES (
    %(id)s,
    %(created_at)s,
    %(menu_id)s,
    %(recipe_version_id)s,
    %(servings)s,
    %(role_option_id)s,
    %(position)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_nutrition_fact.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.nutrition_fact | C | amount, basis_amount, basis_unit_id, created_at, form_id, id, nutrient_id, product_version_id, source_id |

バインド変数: amount, basis_amount, basis_unit_id, created_at, form_id, id, nutrient_id, product_version_id, source_id

```sql
-- 検証済みバックアップの形態・商品別栄養値を元IDと全列で復元する。
INSERT INTO recipeweave.nutrition_fact (
    id,
    created_at,
    form_id,
    product_version_id,
    nutrient_id,
    amount,
    basis_amount,
    basis_unit_id,
    source_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(form_id)s,
    %(product_version_id)s,
    %(nutrient_id)s,
    %(amount)s,
    %(basis_amount)s,
    %(basis_unit_id)s,
    %(source_id)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_pantry_consumption.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.pantry_consumption | C | amount, created_at, id, lot_id, session_id, unit_id, user_id |

バインド変数: amount, created_at, id, lot_id, session_id, unit_id, user_id

```sql
-- 検証済みバックアップの調理による在庫消費の冪等台帳を元IDと全列で復元する。
INSERT INTO recipeweave.pantry_consumption (
    id,
    created_at,
    user_id,
    session_id,
    lot_id,
    amount,
    unit_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(session_id)s,
    %(lot_id)s,
    %(amount)s,
    %(unit_id)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_pantry_lot.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.pantry_lot | C | amount, created_at, edited, expires_on, form_id, id, location, opened_at, original_amount, original_form_id, original_unit_id, priority, product_version_id, quantity_quality, source_import_id, status, unit_id, updated_at, user_id |

バインド変数: amount, created_at, edited, expires_on, form_id, id, location, opened_at, original_amount, original_form_id, original_unit_id, priority, product_version_id, quantity_quality, source_import_id, status, unit_id, updated_at, user_id

```sql
-- 検証済みバックアップの手持ち食材ロットを元IDと全列で復元する。
INSERT INTO recipeweave.pantry_lot (
    id,
    created_at,
    user_id,
    form_id,
    product_version_id,
    amount,
    unit_id,
    expires_on,
    opened_at,
    location,
    priority,
    status,
    source_import_id,
    quantity_quality,
    original_form_id,
    original_amount,
    original_unit_id,
    updated_at,
    edited
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(form_id)s,
    %(product_version_id)s,
    %(amount)s,
    %(unit_id)s,
    %(expires_on)s,
    %(opened_at)s,
    %(location)s,
    %(priority)s,
    %(status)s,
    %(source_import_id)s,
    %(quantity_quality)s,
    %(original_form_id)s,
    %(original_amount)s,
    %(original_unit_id)s,
    %(updated_at)s,
    %(edited)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_product.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.product | C | brand, created_at, food_id, gtin, id, name, status |

バインド変数: brand, created_at, food_id, gtin, id, name, status

```sql
-- 検証済みバックアップの市販商品識別を元IDと全列で復元する。
INSERT INTO recipeweave.product (
    id,
    created_at,
    food_id,
    brand,
    name,
    gtin,
    status
) VALUES (
    %(id)s,
    %(created_at)s,
    %(food_id)s,
    %(brand)s,
    %(name)s,
    %(gtin)s,
    %(status)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_product_allergen.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.product_allergen | C | allergen_id, created_at, id, presence, product_version_id, source_id |

バインド変数: allergen_id, created_at, id, presence, product_version_id, source_id

```sql
-- 検証済みバックアップの商品表示アレルゲンを元IDと全列で復元する。
INSERT INTO recipeweave.product_allergen (
    id,
    created_at,
    product_version_id,
    allergen_id,
    presence,
    source_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(product_version_id)s,
    %(allergen_id)s,
    %(presence)s,
    %(source_id)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_product_component.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.product_component | C | amount, created_at, form_id, id, name, product_version_id, quality, unit_id |

バインド変数: amount, created_at, form_id, id, name, product_version_id, quality, unit_id

```sql
-- 検証済みバックアップのセット内構成品を元IDと全列で復元する。
INSERT INTO recipeweave.product_component (
    id,
    created_at,
    product_version_id,
    form_id,
    name,
    amount,
    unit_id,
    quality
) VALUES (
    %(id)s,
    %(created_at)s,
    %(product_version_id)s,
    %(form_id)s,
    %(name)s,
    %(amount)s,
    %(unit_id)s,
    %(quality)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_product_preparation_rule.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.product_preparation_rule | C | allowed, created_at, id, operation_id, parameter_contract, product_version_id, source_id, use_original_container |

バインド変数: allowed, created_at, id, operation_id, parameter_contract, product_version_id, source_id, use_original_container

```sql
-- 検証済みバックアップの商品固有の調理条件を元IDと全列で復元する。
INSERT INTO recipeweave.product_preparation_rule (
    id,
    created_at,
    product_version_id,
    operation_id,
    allowed,
    use_original_container,
    parameter_contract,
    source_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(product_version_id)s,
    %(operation_id)s,
    %(allowed)s,
    %(use_original_container)s,
    %(parameter_contract)s,
    %(source_id)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_product_version.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.product_version | C | created_at, drain_amount, form_id, id, net_amount, preparation_note, product_id, source_id, unit_id, valid_from, version |

バインド変数: created_at, drain_amount, form_id, id, net_amount, preparation_note, product_id, source_id, unit_id, valid_from, version

```sql
-- 検証済みバックアップの商品仕様版を元IDと全列で復元する。
INSERT INTO recipeweave.product_version (
    id,
    created_at,
    product_id,
    version,
    form_id,
    net_amount,
    unit_id,
    drain_amount,
    source_id,
    preparation_note,
    valid_from
) VALUES (
    %(id)s,
    %(created_at)s,
    %(product_id)s,
    %(version)s,
    %(form_id)s,
    %(net_amount)s,
    %(unit_id)s,
    %(drain_amount)s,
    %(source_id)s,
    %(preparation_note)s,
    %(valid_from)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_receipt_import.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.receipt_import | C | committed_at, created_at, file_sha256, id, idempotency_key, reverted_at, revision, status, undo_preserved_count, user_id |

バインド変数: committed_at, created_at, file_sha256, id, idempotency_key, reverted_at, revision, status, undo_preserved_count, user_id

```sql
-- 検証済みバックアップのレシート読取・在庫登録の処理単位を元IDと全列で復元する。
INSERT INTO recipeweave.receipt_import (
    id,
    created_at,
    user_id,
    file_sha256,
    idempotency_key,
    status,
    revision,
    committed_at,
    reverted_at,
    undo_preserved_count
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(file_sha256)s,
    %(idempotency_key)s,
    %(status)s,
    %(revision)s,
    %(committed_at)s,
    %(reverted_at)s,
    %(undo_preserved_count)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_receipt_line.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.receipt_line | C | amount, created_at, decision, form_id, id, import_id, line_no, pantry_lot_id, product_version_id, raw_name, unit_id |

バインド変数: amount, created_at, decision, form_id, id, import_id, line_no, pantry_lot_id, product_version_id, raw_name, unit_id

```sql
-- 検証済みバックアップのレシートの商品候補と確定した在庫の対応を元IDと全列で復元する。
INSERT INTO recipeweave.receipt_line (
    id,
    created_at,
    import_id,
    line_no,
    raw_name,
    form_id,
    product_version_id,
    amount,
    unit_id,
    decision,
    pantry_lot_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(import_id)s,
    %(line_no)s,
    %(raw_name)s,
    %(form_id)s,
    %(product_version_id)s,
    %(amount)s,
    %(unit_id)s,
    %(decision)s,
    %(pantry_lot_id)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_resource_reservation.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.resource_reservation | C | created_at, end_s, id, quantity, resource_id, start_s, task_id |

バインド変数: created_at, end_s, id, quantity, resource_id, start_s, task_id

```sql
-- 検証済みバックアップの資源の予約を元IDと全列で復元する。
INSERT INTO recipeweave.resource_reservation (
    id,
    created_at,
    task_id,
    resource_id,
    start_s,
    end_s,
    quantity
) VALUES (
    %(id)s,
    %(created_at)s,
    %(task_id)s,
    %(resource_id)s,
    %(start_s)s,
    %(end_s)s,
    %(quantity)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_session_task.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.session_task | C | actual_end_at, actual_start_at, batch_no, confirmed_duration_s, created_at, duration_source, id, menu_item_id, planned_end_s, planned_start_s, session_id, status, step_id, timer_duration_s, timer_started_at |

バインド変数: actual_end_at, actual_start_at, batch_no, confirmed_duration_s, created_at, duration_source, id, menu_item_id, planned_end_s, planned_start_s, session_id, status, step_id, timer_duration_s, timer_started_at

```sql
-- 検証済みバックアップの展開済み工程を元IDと全列で復元する。
INSERT INTO recipeweave.session_task (
    id,
    created_at,
    session_id,
    menu_item_id,
    step_id,
    batch_no,
    planned_start_s,
    planned_end_s,
    status,
    actual_start_at,
    actual_end_at,
    timer_started_at,
    timer_duration_s,
    duration_source,
    confirmed_duration_s
) VALUES (
    %(id)s,
    %(created_at)s,
    %(session_id)s,
    %(menu_item_id)s,
    %(step_id)s,
    %(batch_no)s,
    %(planned_start_s)s,
    %(planned_end_s)s,
    %(status)s,
    %(actual_start_at)s,
    %(actual_end_at)s,
    %(timer_started_at)s,
    %(timer_duration_s)s,
    %(duration_source)s,
    %(confirmed_duration_s)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_shopping_item.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.shopping_item | C | archived, checked, checked_at, client_key, created_at, id, net_shortage, package_count, product_version_id, session_id, surplus_amount, total_id |

バインド変数: archived, checked, checked_at, client_key, created_at, id, net_shortage, package_count, product_version_id, session_id, surplus_amount, total_id

```sql
-- 検証済みバックアップの買い物行を元IDと全列で復元する。
INSERT INTO recipeweave.shopping_item (
    id,
    created_at,
    session_id,
    total_id,
    product_version_id,
    net_shortage,
    package_count,
    surplus_amount,
    checked,
    client_key,
    checked_at,
    archived
) VALUES (
    %(id)s,
    %(created_at)s,
    %(session_id)s,
    %(total_id)s,
    %(product_version_id)s,
    %(net_shortage)s,
    %(package_count)s,
    %(surplus_amount)s,
    %(checked)s,
    %(client_key)s,
    %(checked_at)s,
    %(archived)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_task_dependency.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.task_dependency | C | after_task_id, before_task_id, created_at, id, max_lag_s, min_lag_s, reason |

バインド変数: after_task_id, before_task_id, created_at, id, max_lag_s, min_lag_s, reason

```sql
-- 検証済みバックアップの献立展開後依存を元IDと全列で復元する。
INSERT INTO recipeweave.task_dependency (
    id,
    created_at,
    before_task_id,
    after_task_id,
    min_lag_s,
    max_lag_s,
    reason
) VALUES (
    %(id)s,
    %(created_at)s,
    %(before_task_id)s,
    %(after_task_id)s,
    %(min_lag_s)s,
    %(max_lag_s)s,
    %(reason)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_user_exclusion.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.user_exclusion | C | allergen_id, created_at, food_id, id, strict, user_id |

バインド変数: allergen_id, created_at, food_id, id, strict, user_id

```sql
-- 検証済みバックアップの避けたい食材・物質を元IDと全列で復元する。
INSERT INTO recipeweave.user_exclusion (
    id,
    created_at,
    user_id,
    food_id,
    allergen_id,
    strict
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(food_id)s,
    %(allergen_id)s,
    %(strict)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_user_food.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.user_food | C | created_at, food_id, id, user_id |

バインド変数: created_at, food_id, id, user_id

```sql
-- 検証済みバックアップの利用者が追加した独自食材の所有を元IDと全列で復元する。
INSERT INTO recipeweave.user_food (
    id,
    created_at,
    user_id,
    food_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(food_id)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_user_pantry_food.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.user_pantry_food | C | created_at, food_id, id, user_id |

バインド変数: created_at, food_id, id, user_id

```sql
-- 検証済みバックアップの利用者が常備すると設定した食材を元IDと全列で復元する。
INSERT INTO recipeweave.user_pantry_food (
    id,
    created_at,
    user_id,
    food_id
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(food_id)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_user_preference.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.user_preference | C | created_at, id, option_id, user_id, weight |

バインド変数: created_at, id, option_id, user_id, weight

```sql
-- 検証済みバックアップのユーザーの嗜好を元IDと全列で復元する。
INSERT INTO recipeweave.user_preference (
    id,
    created_at,
    user_id,
    option_id,
    weight
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(option_id)s,
    %(weight)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_user_recipe_event.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.user_recipe_event | C | created_at, id, kind, occurred_at, recipe_version_id, request_key, user_id |

バインド変数: created_at, id, kind, occurred_at, recipe_version_id, request_key, user_id

```sql
-- 検証済みバックアップの提案・調理履歴を元IDと全列で復元する。
INSERT INTO recipeweave.user_recipe_event (
    id,
    created_at,
    user_id,
    recipe_version_id,
    kind,
    occurred_at,
    request_key
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(recipe_version_id)s,
    %(kind)s,
    %(occurred_at)s,
    %(request_key)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q200_insert_user_shopping_check.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.user_shopping_check | C | amount, archived, checked_at, created_at, food_id, id, key, signature, unit_id, user_id |

バインド変数: amount, archived, checked_at, created_at, food_id, id, key, signature, unit_id, user_id

```sql
-- 検証済みバックアップの調理前の買い物確認を元IDと全列で復元する。
INSERT INTO recipeweave.user_shopping_check (
    id,
    created_at,
    user_id,
    key,
    signature,
    food_id,
    amount,
    unit_id,
    checked_at,
    archived
) VALUES (
    %(id)s,
    %(created_at)s,
    %(user_id)s,
    %(key)s,
    %(signature)s,
    %(food_id)s,
    %(amount)s,
    %(unit_id)s,
    %(checked_at)s,
    %(archived)s
);
```

## backend/src/app/apis/backup/preview_backup/sql/q300_reference_allergen.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.allergen | R | id |

バインド変数: reference_ids

```sql
-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.allergen AS t
WHERE t.id = ANY(%(reference_ids)s::UUID[]) AND (TRUE);
```

## backend/src/app/apis/backup/preview_backup/sql/q300_reference_axis_option.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.axis_option | R | id |

バインド変数: reference_ids

```sql
-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.axis_option AS t
WHERE t.id = ANY(%(reference_ids)s::UUID[]) AND (TRUE);
```

## backend/src/app/apis/backup/preview_backup/sql/q300_reference_catalog_release.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.catalog_release | R | id, owner_id |

バインド変数: reference_ids

```sql
-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.catalog_release AS t
WHERE t.id = ANY(%(reference_ids)s::UUID[]) AND (t.owner_id IS NULL);
```

## backend/src/app/apis/backup/preview_backup/sql/q300_reference_food.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | R | id, owner_id |

バインド変数: reference_ids

```sql
-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.food AS t
WHERE t.id = ANY(%(reference_ids)s::UUID[]) AND (t.owner_id IS NULL);
```

## backend/src/app/apis/backup/preview_backup/sql/q300_reference_food_form.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | R | id, owner_id |
| recipeweave.food_form | R | food_id, id |

バインド変数: reference_ids

```sql
-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.food_form AS t
WHERE
    t.id = ANY(%(reference_ids)s::UUID[]) AND (EXISTS (
        SELECT 1 FROM recipeweave.food AS food
        WHERE food.id = t.food_id AND food.owner_id IS NULL
    ));
```

## backend/src/app/apis/backup/preview_backup/sql/q300_reference_nutrient.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.nutrient | R | id |

バインド変数: reference_ids

```sql
-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.nutrient AS t
WHERE t.id = ANY(%(reference_ids)s::UUID[]) AND (TRUE);
```

## backend/src/app/apis/backup/preview_backup/sql/q300_reference_operation.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.operation | R | id |

バインド変数: reference_ids

```sql
-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.operation AS t
WHERE t.id = ANY(%(reference_ids)s::UUID[]) AND (TRUE);
```

## backend/src/app/apis/backup/preview_backup/sql/q300_reference_product.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | R | id, owner_id |
| recipeweave.product | R | food_id, id |

バインド変数: reference_ids

```sql
-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.product AS t
WHERE
    t.id = ANY(%(reference_ids)s::UUID[]) AND (EXISTS (
        SELECT 1 FROM recipeweave.food AS food
        WHERE food.id = t.food_id AND food.owner_id IS NULL
    ));
```

## backend/src/app/apis/backup/preview_backup/sql/q300_reference_product_version.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | R | id, owner_id |
| recipeweave.product | R | food_id, id |
| recipeweave.product_version | R | id, product_id |

バインド変数: reference_ids

```sql
-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.product_version AS t
WHERE
    t.id = ANY(%(reference_ids)s::UUID[])
    AND (EXISTS (
        SELECT 1
        FROM recipeweave.food AS food
        INNER JOIN recipeweave.product AS product ON food.id = product.food_id
        WHERE product.id = t.product_id AND food.owner_id IS NULL
    ));
```

## backend/src/app/apis/backup/preview_backup/sql/q300_reference_recipe_ingredient.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.recipe_ingredient | R | id |

バインド変数: reference_ids

```sql
-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.recipe_ingredient AS t
WHERE t.id = ANY(%(reference_ids)s::UUID[]) AND (TRUE);
```

## backend/src/app/apis/backup/preview_backup/sql/q300_reference_recipe_step.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.recipe_step | R | id |

バインド変数: reference_ids

```sql
-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.recipe_step AS t
WHERE t.id = ANY(%(reference_ids)s::UUID[]) AND (TRUE);
```

## backend/src/app/apis/backup/preview_backup/sql/q300_reference_recipe_version.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.recipe_version | R | id |

バインド変数: reference_ids

```sql
-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.recipe_version AS t
WHERE t.id = ANY(%(reference_ids)s::UUID[]) AND (TRUE);
```

## backend/src/app/apis/backup/preview_backup/sql/q300_reference_resource_type.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.resource_type | R | id |

バインド変数: reference_ids

```sql
-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.resource_type AS t
WHERE t.id = ANY(%(reference_ids)s::UUID[]) AND (TRUE);
```

## backend/src/app/apis/backup/preview_backup/sql/q300_reference_source_record.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.source_record | R | id |

バインド変数: reference_ids

```sql
-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.source_record AS t
WHERE t.id = ANY(%(reference_ids)s::UUID[]) AND (TRUE);
```

## backend/src/app/apis/backup/preview_backup/sql/q300_reference_unit.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.unit | R | id |

バインド変数: reference_ids

```sql
-- 復元する私有行以外の参照は、保持する共有カタログの実在行に限定する。
SELECT t.id FROM recipeweave.unit AS t
WHERE t.id = ANY(%(reference_ids)s::UUID[]) AND (TRUE);
```

## backend/src/app/apis/backup/preview_backup/sql/q800_constraints_immediate.sql

実行条件: このSQLの呼出し経路で実行

保留していた遅延可能な制約を直ちに検査し、以後も即時検査する。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|

バインド変数: なし

```sql
-- 保存直前に遅延FK・制約トリガーをすべて検証する。
SET CONSTRAINTS ALL IMMEDIATE;
```

## backend/src/app/apis/backup/preview_backup/sql/q801_constraints_deferred.sql

実行条件: このSQLの呼出し経路で実行

遅延可能な制約の検査をトランザクション終了まで遅延する。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|

バインド変数: なし

```sql
-- 復元する依存行の挿入順を組み立てる間は遅延可能な制約を保留する。
SET CONSTRAINTS ALL DEFERRED;
```

## backend/src/app/apis/backup/preview_backup/sql/q802_restore_profile.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.app_user | U | id, locale, timezone |

バインド変数: actor_id, locale, timezone

```sql
-- 本人の言語とタイムゾーンだけを復元し、認証主体とアカウント状態は保持する。
UPDATE recipeweave.app_user SET locale = %(locale)s, timezone = %(timezone)s
WHERE id = %(actor_id)s;
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
