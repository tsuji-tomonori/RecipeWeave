# SQL仕様: preview_cooking_plan

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## backend/src/app/apis/workspace/preview_cooking_plan/sql/q001_steps.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.recipe_ingredient | R | recipe_version_id, scaling_rule_id |
| recipeweave.recipe_step | R | attention, duration_max_s, id, recipe_version_id, scaling_rule_id, step_no |
| recipeweave.recipe_version | R | base_servings, id, recipe_id |
| recipeweave.scaling_rule | R | batch_capacity, id, max_servings, min_servings, mode |

バインド変数: item_id, position, servings, version_id

```sql
-- 指定料理版の工程を要求の献立行IDへ対応させる。永続行は作成しない。
SELECT
    %(item_id)s::UUID AS item_id,
    %(position)s::INTEGER AS position,
    %(servings)s::NUMERIC AS servings,
    rv.base_servings,
    rv.recipe_id,
    st.id AS step_id,
    st.step_no,
    st.duration_max_s,
    st.attention,
    sc.mode AS scaling_mode,
    sc.batch_capacity,
    GREATEST(sc.min_servings, (
        SELECT MAX(ingredient_rule.min_servings)
        FROM recipeweave.recipe_ingredient AS ingredient
        INNER JOIN recipeweave.scaling_rule AS ingredient_rule
            ON ingredient.scaling_rule_id = ingredient_rule.id
        WHERE ingredient.recipe_version_id = rv.id
    )) AS min_servings,
    LEAST(sc.max_servings, (
        SELECT MIN(ingredient_rule.max_servings)
        FROM recipeweave.recipe_ingredient AS ingredient
        INNER JOIN recipeweave.scaling_rule AS ingredient_rule
            ON ingredient.scaling_rule_id = ingredient_rule.id
        WHERE ingredient.recipe_version_id = rv.id
    )) AS max_servings
FROM recipeweave.recipe_version AS rv
INNER JOIN recipeweave.recipe_step AS st ON rv.id = st.recipe_version_id
INNER JOIN recipeweave.scaling_rule AS sc ON st.scaling_rule_id = sc.id
WHERE rv.id = %(version_id)s
ORDER BY st.step_no;
```

## backend/src/app/apis/workspace/preview_cooking_plan/sql/q002_dependencies.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.recipe_step | R | id, recipe_version_id |
| recipeweave.step_dependency | R | after_step_id, before_step_id, id, kind, max_lag_s, min_lag_s |

バインド変数: item_id, version_id

```sql
-- 指定料理版の安全・材料・品質に基づく先行条件を読む。
SELECT
    %(item_id)s::UUID AS item_id,
    d.before_step_id,
    d.after_step_id,
    d.min_lag_s,
    d.max_lag_s,
    d.kind
FROM recipeweave.recipe_step AS st
INNER JOIN recipeweave.step_dependency AS d ON st.id = d.after_step_id
WHERE st.recipe_version_id = %(version_id)s
ORDER BY d.id;
```

## backend/src/app/apis/workspace/preview_cooking_plan/sql/q003_requirements.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.recipe_step | R | id, recipe_version_id |
| recipeweave.resource_type | R | code, id, name |
| recipeweave.step_resource | R | capacity_min, exclusive, quantity, resource_type_id, step_id |

バインド変数: version_id

```sql
-- 工程が必要とする器具の台数と単位容量を読む。
SELECT
    sr.step_id,
    sr.resource_type_id,
    sr.quantity,
    sr.capacity_min,
    sr.exclusive,
    rt.name,
    rt.code
FROM recipeweave.step_resource AS sr
INNER JOIN recipeweave.recipe_step AS st ON sr.step_id = st.id
INNER JOIN recipeweave.resource_type AS rt ON sr.resource_type_id = rt.id
WHERE st.recipe_version_id = %(version_id)s
ORDER BY sr.step_id, rt.code;
```

## backend/src/app/apis/workspace/preview_cooking_plan/sql/q004_resources.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.kitchen_resource | R | active, capacity, id, name, quantity, resource_type_id, user_id |
| recipeweave.resource_type | R | code, id |

バインド変数: user_id

```sql
-- 本人が登録した実際の設備数と容量を読む。
SELECT
    k.id,
    k.resource_type_id,
    k.name,
    k.quantity,
    k.capacity,
    rt.code
FROM recipeweave.kitchen_resource AS k
INNER JOIN recipeweave.resource_type AS rt ON k.resource_type_id = rt.id
WHERE k.user_id = %(user_id)s AND k.active
ORDER BY rt.code, k.id;
```

## backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql

実行条件: 共有処理 get_recipe を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.axis_option | R | id, label |
| recipeweave.compatibility_rule | R | code, id |
| recipeweave.food_form | R | food_id, id, name |
| recipeweave.menu | R | id, user_id |
| recipeweave.menu_item | R | menu_id, recipe_version_id |
| recipeweave.operation | R | code, id, name |
| recipeweave.recipe | R | id, status, title, withdrawal_reason |
| recipeweave.recipe_ingredient | R | amount, form_id, id, line_no, note, product_version_id, recipe_version_id, unit_id |
| recipeweave.recipe_option | R | option_id, recipe_version_id |
| recipeweave.recipe_step | R | attention, duration_max_s, id, instruction, operation_id, recipe_version_id, scaling_rule_id, step_no, title |
| recipeweave.recipe_version | R | base_servings, description, id, recipe_id, status, validation, version |
| recipeweave.resource_type | R | code, id, name |
| recipeweave.scaling_rule | R | id, mode |
| recipeweave.step_resource | R | resource_type_id, step_id |
| recipeweave.unit | R | code, id |
| recipeweave.user_recipe_event | R | recipe_version_id, user_id |
| recipeweave.validation_result | R | recipe_version_id, rule_id, state |

バインド変数: equipment, exclude_id, excluded_food_ids, limit, match, max_minutes, offset, owner_id, preview, q, recipe_id, selected_food_ids, version_id

```sql
-- 指定したレシピの数量・分類・工程・資源を正規化テーブルから取得する。
WITH owned_versions AS (
    SELECT menu_item.recipe_version_id AS version_id
    FROM recipeweave.menu_item AS menu_item
    INNER JOIN recipeweave.menu AS menu ON menu_item.menu_id = menu.id
    WHERE menu.user_id = %(owner_id)s::UUID
    UNION
    SELECT user_recipe_event.recipe_version_id AS version_id
    FROM recipeweave.user_recipe_event AS user_recipe_event
    WHERE user_recipe_event.user_id = %(owner_id)s::UUID
),

candidate AS (
    SELECT
        recipe.id,
        recipe.title,
        recipe.status AS recipe_status,
        recipe.withdrawal_reason,
        recipe_view.id AS version_id,
        recipe_view.description,
        recipe_view.base_servings,
        recipe_view.status AS version_status,
        recipe_view.validation,
        COALESCE((
            SELECT SUM(recipe_step.duration_max_s)
            FROM recipeweave.recipe_step AS recipe_step
            WHERE recipe_step.recipe_version_id = recipe_view.id
        ), 0) / 60.0 AS minutes
    FROM recipeweave.recipe AS recipe
    INNER JOIN LATERAL (
        SELECT
            recipe_version.id,
            recipe_version.description,
            recipe_version.base_servings,
            recipe_version.status,
            recipe_version.validation
        FROM recipeweave.recipe_version AS recipe_version
        WHERE
            recipe_version.recipe_id = recipe.id
            AND (%(version_id)s::UUID IS NULL OR recipe_version.id = %(version_id)s::UUID)
            AND (
                (recipe_version.status = 'published' AND recipe_version.validation = 'passed')
                OR (%(preview)s AND recipe_version.status = 'draft')
                OR EXISTS (
                    SELECT 1 FROM owned_versions
                    WHERE owned_versions.version_id = recipe_version.id
                )
            )
        ORDER BY recipe_version.version DESC
        LIMIT 1
    ) AS recipe_view ON TRUE
    WHERE
        recipe.status = 'published' OR (%(preview)s AND recipe.status = 'draft')
        OR EXISTS (
            SELECT 1 FROM owned_versions
            WHERE owned_versions.version_id = recipe_view.id
        )
),

matched AS (
    SELECT
        candidate.id,
        candidate.title,
        candidate.recipe_status,
        candidate.withdrawal_reason,
        candidate.version_id,
        candidate.description,
        candidate.base_servings,
        candidate.version_status,
        candidate.validation,
        candidate.minutes
    FROM candidate
    WHERE (%(q)s = '' OR STRPOS(
        LOWER(candidate.title || ' ' || candidate.description),
        LOWER(%(q)s)
    ) > 0)
    AND (%(recipe_id)s::UUID IS NULL OR candidate.id = %(recipe_id)s::UUID)
    AND (%(exclude_id)s::UUID IS NULL OR candidate.id <> %(exclude_id)s::UUID)
    AND (%(max_minutes)s::NUMERIC IS NULL OR candidate.minutes <= %(max_minutes)s)
    AND (
        CARDINALITY(%(selected_food_ids)s::UUID[]) = 0
        OR (%(match)s = 'any' AND EXISTS (
            SELECT 1 FROM recipeweave.recipe_ingredient AS selected_ingredient
            INNER JOIN recipeweave.food_form AS selected_form
                ON selected_ingredient.form_id = selected_form.id
            WHERE
                selected_ingredient.recipe_version_id = candidate.version_id
                AND selected_form.food_id = ANY(%(selected_food_ids)s::UUID[])
        )) OR (%(match)s = 'all' AND NOT EXISTS (
            SELECT 1 FROM UNNEST(%(selected_food_ids)s::UUID[]) AS requested (food_id)
            WHERE NOT EXISTS (
                SELECT 1 FROM recipeweave.recipe_ingredient AS all_ingredient
                INNER JOIN recipeweave.food_form AS all_form
                    ON all_ingredient.form_id = all_form.id
                WHERE
                    all_ingredient.recipe_version_id = candidate.version_id
                    AND all_form.food_id = requested.food_id
            )
        ))
    )
    AND NOT EXISTS (
        SELECT 1 FROM recipeweave.recipe_ingredient AS excluded_ingredient
        INNER JOIN recipeweave.food_form AS excluded_form
            ON excluded_ingredient.form_id = excluded_form.id
        WHERE
            excluded_ingredient.recipe_version_id = candidate.version_id
            AND excluded_form.food_id = ANY(%(excluded_food_ids)s::UUID[])
    )
    AND (CARDINALITY(%(equipment)s::TEXT[]) = 0 OR NOT EXISTS (
        SELECT 1 FROM recipeweave.recipe_step AS equipment_step
        INNER JOIN recipeweave.step_resource AS equipment_usage
            ON equipment_step.id = equipment_usage.step_id
        INNER JOIN recipeweave.resource_type AS equipment_type
            ON equipment_usage.resource_type_id = equipment_type.id
        WHERE
            equipment_step.recipe_version_id = candidate.version_id
            AND equipment_type.code NOT IN ('person', 'burner', 'knife', 'bowl')
            AND NOT (equipment_type.name = ANY(%(equipment)s::TEXT[]))
    ))
),

page AS (
    SELECT
        matched.id,
        matched.title,
        matched.recipe_status,
        matched.withdrawal_reason,
        matched.version_id,
        matched.description,
        matched.base_servings,
        matched.version_status,
        matched.validation,
        matched.minutes
    FROM matched
    ORDER BY matched.title, matched.id
    LIMIT %(limit)s OFFSET %(offset)s
),

payloads AS (
    SELECT
        page.id,
        page.title,
        JSONB_BUILD_OBJECT(
            'id', page.id::TEXT, 'name', page.title, 'description', page.description,
            'versionId', page.version_id::TEXT,
            'publicationStatus', CASE
                WHEN page.recipe_status = 'withdrawn'
                    THEN 'withdrawn'
                ELSE page.version_status
            END,
            'withdrawalReason', page.withdrawal_reason,
            'servings', page.base_servings, 'minutes', page.minutes,
            'equipment', COALESCE((
                SELECT JSONB_AGG(DISTINCT equipment_type.name)
                FROM recipeweave.recipe_step AS equipment_step
                INNER JOIN recipeweave.step_resource AS equipment_usage
                    ON equipment_step.id = equipment_usage.step_id
                INNER JOIN recipeweave.resource_type AS equipment_type
                    ON equipment_usage.resource_type_id = equipment_type.id
                WHERE
                    equipment_step.recipe_version_id = page.version_id
                    AND equipment_type.code NOT IN ('person', 'burner', 'knife', 'bowl')
            ), '[]'::JSONB),
            'ingredients', COALESCE((
                SELECT
                    JSONB_AGG(JSONB_BUILD_OBJECT(
                        'ingredientId', ingredient.id::TEXT,
                        'formId', ingredient.form_id::TEXT,
                        'productVersionId', ingredient.product_version_id::TEXT,
                        'foodId', form.food_id::TEXT,
                        'quantity',
                        JSONB_BUILD_OBJECT('value', ingredient.amount, 'unit', unit.code),
                        'form', form.name, 'note', COALESCE(ingredient.note, '')
                    ) ORDER BY ingredient.line_no)
                FROM recipeweave.recipe_ingredient AS ingredient
                INNER JOIN recipeweave.food_form AS form ON ingredient.form_id = form.id
                INNER JOIN recipeweave.unit AS unit ON ingredient.unit_id = unit.id
                WHERE ingredient.recipe_version_id = page.version_id
            ), '[]'::JSONB),
            'steps', COALESCE((
                SELECT
                    JSONB_AGG(JSONB_BUILD_OBJECT(
                        'id', step.id::TEXT, 'title', step.title, 'instruction', step.instruction,
                        'minutes', step.duration_max_s / 60.0, 'mode', step.attention,
                        'timeScalingMode', time_rule.mode,
                        'equipment', COALESCE((
                            SELECT JSONB_AGG(resource_kind.name ORDER BY resource_kind.name)
                            FROM recipeweave.step_resource AS resource_usage
                            INNER JOIN recipeweave.resource_type AS resource_kind
                                ON resource_usage.resource_type_id = resource_kind.id
                            WHERE
                                resource_usage.step_id = step.id
                                AND resource_kind.code NOT IN ('person', 'burner')
                        ), '[]'::JSONB),
                        'guide', CASE
                            WHEN LEFT(cook_operation.code, 4) = 'cut_'
                                THEN cook_operation.name
                        END
                    ) ORDER BY step.step_no)
                FROM recipeweave.recipe_step AS step
                INNER JOIN
                    recipeweave.operation AS cook_operation
                    ON step.operation_id = cook_operation.id
                INNER JOIN
                    recipeweave.scaling_rule AS time_rule
                    ON step.scaling_rule_id = time_rule.id
                WHERE step.recipe_version_id = page.version_id
            ), '[]'::JSONB),
            'arrangementIds', '[]'::JSONB,
            'tags', COALESCE((
                SELECT JSONB_AGG(facet_value.label ORDER BY facet_value.label)
                FROM recipeweave.recipe_option AS relation
                INNER JOIN
                    recipeweave.axis_option AS facet_value
                    ON relation.option_id = facet_value.id
                WHERE relation.recipe_version_id = page.version_id
            ), '[]'::JSONB),
            'sample', page.version_status <> 'published' OR EXISTS (
                SELECT 1 FROM recipeweave.validation_result AS validation_row
                INNER JOIN
                    recipeweave.compatibility_rule AS validation_rule
                    ON validation_row.rule_id = validation_rule.id
                WHERE
                    validation_row.recipe_version_id = page.version_id
                    AND validation_rule.code = 'cooking_trial'
                    AND validation_row.state <> 'passed'
            ),
            'imageUrl', NULL
        ) AS payload
    FROM page
)

SELECT
    COALESCE(
        JSONB_AGG(payloads.payload ORDER BY payloads.title, payloads.id),
        '[]'::JSONB
    ) AS items,
    (SELECT COUNT(matched.id) FROM matched) AS total
FROM payloads;
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
