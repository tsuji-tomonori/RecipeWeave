# SQL仕様: update_menu_item

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## backend/src/app/apis/workspace/update_menu_item/sql/q001_delete_item.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.menu | R | id, user_id |
| recipeweave.menu_item | D | id, menu_id |

バインド変数: menu_id, row_id, user_id

```sql
-- 本人の現在の献立の料理を外す。調理中の入力は専用の献立版へ保存する。
DELETE FROM recipeweave.menu_item
WHERE
    id = %(row_id)s AND menu_id = %(menu_id)s
    AND EXISTS (
        SELECT 1 FROM recipeweave.menu AS m
        WHERE m.id = %(menu_id)s AND m.user_id = %(user_id)s
    )
RETURNING id;
```

## backend/src/app/apis/workspace/update_menu_item/sql/q010_recipe.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.axis | R | code, id |
| recipeweave.axis_option | R | axis_id, id |
| recipeweave.recipe | R | id, status |
| recipeweave.recipe_option | R | option_id, recipe_version_id |
| recipeweave.recipe_version | R | base_servings, id, recipe_id, status, validation, version |

バインド変数: preview, recipe_id, requested_version_id

```sql
-- 公開済み料理、または明示したローカル試用で利用できる料理版を選ぶ。
SELECT
    rv.id,
    rv.base_servings,
    ARRAY(
        SELECT ao.id FROM recipeweave.recipe_option AS ro
        INNER JOIN recipeweave.axis_option AS ao ON ro.option_id = ao.id
        INNER JOIN recipeweave.axis AS ax ON ao.axis_id = ax.id
        WHERE ro.recipe_version_id = rv.id AND ax.code = 'dish_role'
        ORDER BY ao.id
    ) AS role_option_ids
FROM recipeweave.recipe_version AS rv
INNER JOIN
    recipeweave.recipe AS r
    ON rv.recipe_id = r.id
WHERE
    r.id = %(recipe_id)s
    AND (%(requested_version_id)s::UUID IS NULL OR rv.id = %(requested_version_id)s)
    AND (
        (rv.status = 'published' AND rv.validation = 'passed' AND r.status = 'published')
        OR (%(preview)s AND rv.status = 'draft' AND r.status = 'draft')
    )
ORDER BY rv.version DESC
LIMIT 1;
```

## backend/src/app/apis/workspace/update_menu_item/sql/q011_ingredients.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food_form | R | food_id, id |
| recipeweave.recipe_ingredient | R | amount, form_id, id, line_no, optional, recipe_version_id, unit_id |
| recipeweave.unit | R | code, id |

バインド変数: version_id

```sql
-- 指定料理の材料ID・単位・基準量を照合する。
SELECT
    ri.id,
    fm.food_id,
    ri.amount,
    ri.optional,
    ri.unit_id,
    ri.form_id,
    u.code AS unit
FROM recipeweave.recipe_ingredient AS ri
INNER JOIN recipeweave.food_form AS fm ON ri.form_id = fm.id
INNER JOIN recipeweave.unit AS u ON ri.unit_id = u.id
WHERE ri.recipe_version_id = %(version_id)s
ORDER BY ri.line_no;
```

## backend/src/app/apis/workspace/update_menu_item/sql/q012_menu.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.menu | C | id, name, revision, servings, user_id |

バインド変数: menu_id, name, user_id

```sql
-- 現在の献立を初回だけ作成し、所有者を固定する。
INSERT INTO recipeweave.menu (id, user_id, name, servings, revision)
VALUES (%(menu_id)s, %(user_id)s, %(name)s, 2, 1) ON CONFLICT (id) DO NOTHING;
```

## backend/src/app/apis/workspace/update_menu_item/sql/q013_insert_item.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.menu_item | C,R | id, menu_id, position, recipe_version_id, role_option_id, servings |

バインド変数: menu_id, role_option_id, row_id, servings, version_id

```sql
-- 検証した料理版と人数を献立へ登録する。
INSERT INTO recipeweave.menu_item (
    id, menu_id, recipe_version_id, servings, role_option_id, position
)
VALUES (
    %(row_id)s, %(menu_id)s, %(version_id)s, %(servings)s, %(role_option_id)s,
    (
        SELECT COALESCE(MAX(mi.position), 0) + 1 FROM recipeweave.menu_item AS mi
        WHERE mi.menu_id = %(menu_id)s
    )
)
RETURNING id;
```

## backend/src/app/apis/workspace/update_menu_item/sql/q014_override.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.menu_ingredient_override | C | amount, form_id, id, ingredient_line_id, menu_item_id, product_version_id, selected |

バインド変数: amount, ingredient_id, item_id, row_id, selected

```sql
-- 利用者が確認した確定分量だけを元の材料行へ結び付ける。
INSERT INTO recipeweave.menu_ingredient_override (
    id, menu_item_id, ingredient_line_id, selected, amount, form_id, product_version_id
)
VALUES (%(row_id)s, %(item_id)s, %(ingredient_id)s, %(selected)s, %(amount)s, NULL, NULL);
```

## backend/src/app/apis/workspace/update_menu_item/sql/q015_advance_menu.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.menu | U | id, revision, user_id |

バインド変数: menu_id, user_id

```sql
-- 調理計画が参照する献立版を更新する。
UPDATE recipeweave.menu SET revision = revision + 1
WHERE id = %(menu_id)s AND user_id = %(user_id)s RETURNING revision;
```

## backend/src/app/apis/workspace/update_menu_item/sql/q900_lock_revision.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.workspace_revision | R | revision, user_id |

バインド変数: user_id

```sql
-- 本人の集約版を排他ロックして並行操作の順序を確定する。
SELECT revision FROM recipeweave.workspace_revision
WHERE user_id = %(user_id)s FOR UPDATE;
```

## backend/src/app/apis/workspace/update_menu_item/sql/q901_advance_revision.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.workspace_revision | U | revision, user_id |

バインド変数: user_id

```sql
-- 業務行の更新と同じトランザクションで版を一度だけ進める。
UPDATE recipeweave.workspace_revision SET revision = revision + 1
WHERE user_id = %(user_id)s RETURNING revision;
```

## backend/src/app/apis/workspace/update_menu_item/sql/q902_append_audit.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.audit_event | C | action, actor_id, entity_key_hash, entity_type, id, occurred_at, reason |

バインド変数: action, key_hash, row_id, user_id

```sql
-- 個人データ本文を複製せず操作と対象キーのハッシュを記録する。
INSERT INTO recipeweave.audit_event (
    id, actor_id, action, entity_type, entity_key_hash, reason, occurred_at
)
VALUES (
    %(row_id)s, %(user_id)s, %(action)s, 'workspace', %(key_hash)s,
    '本人の業務操作', CURRENT_TIMESTAMP
);
```

## backend/src/app/apis/workspace/get_workspace/sql/q001_revision.sql

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.workspace_revision | R | revision, user_id |

バインド変数: user_id

```sql
-- 複数表の読取り中に本人の業務更新が割り込まないよう共有ロックする。
SELECT revision FROM recipeweave.workspace_revision
WHERE user_id = %(user_id)s FOR SHARE;
```

## backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food_form | R | food_id, id, name |
| recipeweave.pantry_lot | R | amount, created_at, edited, expires_on, form_id, id, location, original_amount, original_form_id, original_unit_id, priority, source_import_id, status, unit_id, updated_at, user_id |
| recipeweave.unit | R | code, id |

バインド変数: user_id

```sql
-- 在庫本体・登録時の値・食材形態・単位を別々の正規化行から復元する。
SELECT
    p.id,
    f.food_id,
    f.name AS form,
    p.amount,
    u.code AS unit,
    p.original_amount,
    p.location,
    p.priority,
    p.expires_on,
    p.created_at,
    p.updated_at,
    p.source_import_id,
    p.status,
    p.edited,
    COALESCE(ofm.food_id, f.food_id) AS original_food_id,
    COALESCE(ou.code, u.code) AS original_unit
FROM recipeweave.pantry_lot AS p
INNER JOIN recipeweave.food_form AS f ON p.form_id = f.id
INNER JOIN recipeweave.unit AS u ON p.unit_id = u.id
LEFT JOIN recipeweave.food_form AS ofm ON p.original_form_id = ofm.id
LEFT JOIN recipeweave.unit AS ou ON p.original_unit_id = ou.id
WHERE p.user_id = %(user_id)s
ORDER BY p.created_at, p.id;
```

## backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.pantry_consumption | R | amount, created_at, id, lot_id, session_id, unit_id, user_id |
| recipeweave.unit | R | code, id |

バインド変数: user_id

```sql
-- 二重消費を防ぐ台帳からロットごとの使用履歴を読む。
SELECT
    c.lot_id,
    c.amount,
    u.code AS unit,
    c.session_id
FROM recipeweave.pantry_consumption AS c INNER JOIN recipeweave.unit AS u ON c.unit_id = u.id
WHERE c.user_id = %(user_id)s
ORDER BY c.created_at, c.id;
```

## backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.receipt_import | R | created_at, file_sha256, id, idempotency_key, reverted_at, status, user_id |

バインド変数: user_id

```sql
-- 画像本文を保存せず、重複検知と取消しに必要な履歴だけを読む。
SELECT
    r.id,
    r.file_sha256,
    r.idempotency_key,
    r.created_at,
    r.status,
    r.reverted_at
FROM
    recipeweave.receipt_import AS r
WHERE
    r.user_id = %(user_id)s
    AND r.status IN ('committed', 'reverted')
ORDER BY r.created_at, r.id;
```

## backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.menu | R | id, revision, user_id |
| recipeweave.menu_item | R | id, menu_id, position, recipe_version_id, servings |
| recipeweave.recipe_version | R | id, recipe_id |

バインド変数: menu_id, user_id

```sql
-- 現在の献立を固定した本人用IDで読む。
SELECT
    mi.id,
    rv.recipe_id,
    mi.servings,
    mi.recipe_version_id,
    m.revision
FROM recipeweave.menu AS m INNER JOIN recipeweave.menu_item AS mi ON m.id = mi.menu_id
INNER JOIN recipeweave.recipe_version AS rv ON mi.recipe_version_id = rv.id
WHERE m.id = %(menu_id)s AND m.user_id = %(user_id)s
ORDER BY mi.position, mi.id;
```

## backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food_form | R | food_id, id, name |
| recipeweave.menu | R | id, user_id |
| recipeweave.menu_ingredient_override | R | amount, id, ingredient_line_id, menu_item_id, selected |
| recipeweave.menu_item | R | id, menu_id, position, recipe_version_id, servings |
| recipeweave.recipe_ingredient | R | amount, form_id, id, line_no, recipe_version_id, unit_id |
| recipeweave.recipe_version | R | base_servings, id |
| recipeweave.unit | R | code, id |

バインド変数: menu_id, user_id

```sql
-- 献立の確定分量を材料行と上書き行から復元する。
SELECT
    mi.id AS menu_item_id,
    f.food_id,
    f.name AS form,
    ri.id AS ingredient_id,
    u.code AS unit,
    ov.id AS override_id,
    CASE WHEN ov.selected = FALSE THEN 0 ELSE ov.amount END AS override_amount,
    ri.amount * mi.servings / rv.base_servings AS scaled_amount
FROM recipeweave.menu_item AS mi INNER JOIN recipeweave.menu AS m ON mi.menu_id = m.id
INNER JOIN recipeweave.recipe_version AS rv ON mi.recipe_version_id = rv.id
INNER JOIN recipeweave.recipe_ingredient AS ri ON rv.id = ri.recipe_version_id
INNER JOIN recipeweave.food_form AS f ON ri.form_id = f.id
INNER JOIN recipeweave.unit AS u ON ri.unit_id = u.id
LEFT JOIN
    recipeweave.menu_ingredient_override AS ov
    ON mi.id = ov.menu_item_id AND ri.id = ov.ingredient_line_id
WHERE m.id = %(menu_id)s AND m.user_id = %(user_id)s
ORDER BY mi.position, ri.line_no;
```

## backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.recipe_version | R | id, recipe_id |
| recipeweave.user_recipe_event | R | created_at, id, kind, occurred_at, recipe_version_id, user_id |

バインド変数: user_id

```sql
-- 保存と解除の追記イベントから、料理ごとの現在状態を導出する。
SELECT ranked.recipe_id FROM (
    SELECT
        rv.recipe_id,
        ev.kind,
        ROW_NUMBER()
            OVER (
                PARTITION BY rv.recipe_id
                ORDER BY ev.occurred_at DESC, ev.created_at DESC, ev.id DESC
            )
            AS rank
    FROM recipeweave.user_recipe_event AS ev
    INNER JOIN recipeweave.recipe_version AS rv ON ev.recipe_version_id = rv.id
    WHERE ev.user_id = %(user_id)s AND ev.kind IN ('liked', 'disliked')
) AS ranked
WHERE ranked.rank = 1 AND ranked.kind = 'liked'
ORDER BY ranked.recipe_id;
```

## backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.kitchen_resource | R | active, resource_type_id, user_id |
| recipeweave.resource_type | R | code, id, name |
| recipeweave.user_exclusion | R | food_id, user_id |
| recipeweave.user_pantry_food | R | food_id, user_id |

バインド変数: user_id

```sql
-- 除外・常備・器具を各設定表から一覧化する。
SELECT
    'excluded' AS kind,
    food_id::TEXT AS setting_value
FROM recipeweave.user_exclusion
WHERE user_id = %(user_id)s AND food_id IS NOT NULL
UNION ALL
SELECT
    'pantry' AS kind,
    food_id::TEXT AS setting_value
FROM recipeweave.user_pantry_food
WHERE user_id = %(user_id)s
UNION ALL
SELECT
    'equipment' AS kind,
    r.name AS setting_value
FROM recipeweave.kitchen_resource AS k
INNER JOIN recipeweave.resource_type AS r ON k.resource_type_id = r.id
WHERE k.user_id = %(user_id)s AND k.active AND r.code NOT IN ('person', 'burner', 'bowl');
```

## backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food | R | id, name |
| recipeweave.food_form | R | base_unit_id, food_id |
| recipeweave.unit | R | code, id |
| recipeweave.user_food | R | food_id, user_id |

バインド変数: user_id

```sql
-- 本人の独自食材は所有表を経由して取得する。
SELECT
    f.id,
    f.name,
    u.code AS unit
FROM recipeweave.user_food AS uf
INNER JOIN recipeweave.food AS f ON uf.food_id = f.id
INNER JOIN recipeweave.food_form AS fm ON f.id = fm.food_id
INNER JOIN recipeweave.unit AS u ON fm.base_unit_id = u.id
WHERE uf.user_id = %(user_id)s
ORDER BY f.name, f.id;
```

## backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.unit | R | code, id |
| recipeweave.user_shopping_check | R | amount, archived, checked_at, food_id, id, key, signature, unit_id, user_id |

バインド変数: user_id

```sql
-- 調理開始前にも利用できる本人の買い物確認を読む。
SELECT
    c.key AS client_key,
    c.signature,
    c.food_id,
    c.amount,
    u.code AS unit,
    c.checked_at,
    c.archived
FROM recipeweave.user_shopping_check AS c INNER JOIN recipeweave.unit AS u ON c.unit_id = u.id
WHERE c.user_id = %(user_id)s
ORDER BY c.checked_at, c.id;
```

## backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.cooking_session | R | created_at, current_task_index, id, input_snapshot, menu_id, status |
| recipeweave.menu | R | id, user_id |

バインド変数: user_id

```sql
-- 本人の直近の調理を読む。入力の料理はセッション専用献立に固定済み。
SELECT
    s.id,
    s.menu_id,
    s.status,
    s.current_task_index,
    s.input_snapshot
FROM recipeweave.cooking_session AS s INNER JOIN recipeweave.menu AS m ON s.menu_id = m.id
WHERE m.user_id = %(user_id)s AND s.status <> 'cancelled'
ORDER BY s.created_at DESC, s.id DESC
LIMIT 1;
```

## backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.menu_item | R | id, position, recipe_version_id |
| recipeweave.recipe | R | id, title |
| recipeweave.recipe_step | R | attention, duration_max_s, id, instruction, scaling_rule_id, step_no, title |
| recipeweave.recipe_version | R | id, recipe_id |
| recipeweave.scaling_rule | R | id, mode |
| recipeweave.session_task | R | confirmed_duration_s, duration_source, id, menu_item_id, planned_end_s, planned_start_s, session_id, status, step_id, timer_duration_s, timer_started_at |

バインド変数: session_id

```sql
-- 調理工程とタイマーを正規化されたタスクから読む。
SELECT
    t.id,
    t.menu_item_id,
    t.step_id,
    t.planned_start_s,
    t.planned_end_s,
    t.duration_source,
    t.confirmed_duration_s,
    t.status,
    t.timer_started_at,
    t.timer_duration_s,
    rv.recipe_id,
    r.title AS recipe_name,
    st.title,
    st.instruction,
    st.attention,
    st.duration_max_s,
    scaling.mode AS scaling_mode
FROM recipeweave.session_task AS t INNER JOIN recipeweave.menu_item AS mi ON t.menu_item_id = mi.id
INNER JOIN recipeweave.recipe_version AS rv ON mi.recipe_version_id = rv.id
INNER JOIN recipeweave.recipe AS r ON rv.recipe_id = r.id
INNER JOIN recipeweave.recipe_step AS st ON t.step_id = st.id
INNER JOIN recipeweave.scaling_rule AS scaling ON st.scaling_rule_id = scaling.id
WHERE t.session_id = %(session_id)s
ORDER BY t.planned_start_s, mi.position, st.step_no, t.id;
```

## backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.resource_type | R | code, id, name |
| recipeweave.session_task | R | id, session_id, step_id |
| recipeweave.step_resource | R | resource_type_id, step_id |

バインド変数: session_id

```sql
-- タスクに必要な器具の表示名を読む。
SELECT
    t.id AS task_id,
    r.name
FROM recipeweave.session_task AS t
INNER JOIN recipeweave.step_resource AS sr ON t.step_id = sr.step_id
INNER JOIN recipeweave.resource_type AS r ON sr.resource_type_id = r.id
WHERE t.session_id = %(session_id)s AND r.code <> 'person'
ORDER BY t.id, r.name;
```

## backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.food_form | R | food_id, id, name |
| recipeweave.ingredient_total | R | actual_amount, consumption_outcome, form_id, id, product_version_id, required_amount, session_id, unit_id |
| recipeweave.pantry_consumption | R | amount, id, lot_id, session_id |
| recipeweave.pantry_lot | R | form_id, id, product_version_id, unit_id |
| recipeweave.unit | R | code, id |

バインド変数: session_id

```sql
-- 使用量の結果は合計表と消費台帳から導出する。
SELECT
    total.id,
    fm.food_id,
    fm.name AS form,
    total.required_amount,
    total.actual_amount,
    total.consumption_outcome,
    u.code AS unit,
    COALESCE(SUM(c.amount), 0) AS consumed_amount,
    ARRAY_AGG(c.lot_id) FILTER (WHERE c.id IS NOT NULL) AS lot_ids
FROM recipeweave.ingredient_total AS total
INNER JOIN recipeweave.food_form AS fm ON total.form_id = fm.id
INNER JOIN recipeweave.unit AS u ON total.unit_id = u.id
LEFT JOIN recipeweave.pantry_lot AS p
    ON
        total.form_id = p.form_id AND total.unit_id = p.unit_id
        AND total.product_version_id IS NOT DISTINCT FROM p.product_version_id
LEFT JOIN recipeweave.pantry_consumption AS c ON p.id = c.lot_id AND total.session_id = c.session_id
WHERE total.session_id = %(session_id)s
GROUP BY total.id, fm.food_id, fm.name, u.code
ORDER BY total.id;
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
