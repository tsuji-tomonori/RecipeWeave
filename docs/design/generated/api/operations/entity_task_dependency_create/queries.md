# SQL仕様: entity_task_dependency_create

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

## backend/src/app/apis/entities/task_dependency_create/sql/001_create.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.task_dependency | C | after_task_id, before_task_id, created_at, id, max_lag_s, min_lag_s, reason, xmin |

バインド変数: after_task_id, before_task_id, max_lag_s, min_lag_s, reason, row_id

```sql
-- 献立展開後依存を作成する。
-- 値は名前付きパラメータで束縛する。
INSERT INTO recipeweave.task_dependency AS t (
    id,
    before_task_id,
    after_task_id,
    min_lag_s,
    max_lag_s,
    reason
)
VALUES (
    %(row_id)s,
    %(before_task_id)s,
    %(after_task_id)s,
    %(min_lag_s)s,
    %(max_lag_s)s,
    %(reason)s
)
RETURNING
    t.id,
    t.created_at,
    t.before_task_id,
    t.after_task_id,
    t.min_lag_s,
    t.max_lag_s,
    t.reason,
    t.xmin::TEXT AS etag;
```

## backend/src/app/apis/entities/task_dependency_create/sql/002_reference_before_task_id.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.cooking_session | R | id, menu_id |
| recipeweave.menu | R | id, user_id |
| recipeweave.session_task | R | id, session_id |

バインド変数: actor_id, reference_id

```sql
-- 参照先の展開済み工程が同じ利用者に属することを検証する。
SELECT t.id FROM recipeweave.session_task AS t
WHERE
    t.id = %(reference_id)s
    AND EXISTS (
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
    );
```

## backend/src/app/apis/entities/task_dependency_create/sql/003_reference_after_task_id.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.cooking_session | R | id, menu_id |
| recipeweave.menu | R | id, user_id |
| recipeweave.session_task | R | id, session_id |

バインド変数: actor_id, reference_id

```sql
-- 参照先の展開済み工程が同じ利用者に属することを検証する。
SELECT t.id FROM recipeweave.session_task AS t
WHERE
    t.id = %(reference_id)s
    AND EXISTS (
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
    );
```

## backend/src/app/entities/sql/audit.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.audit_event | C | action, actor_id, entity_key_hash, entity_type, id, occurred_at, reason |

バインド変数: action, actor_id, entity_key_hash, entity_type, row_id

```sql
-- 個人本文を複製せず、同じ業務トランザクションで変更履歴を追記する。
INSERT INTO recipeweave.audit_event (
    id, actor_id, action, entity_type, entity_key_hash, reason, occurred_at
)
VALUES (
    %(row_id)s, %(actor_id)s, %(action)s, %(entity_type)s,
    %(entity_key_hash)s, 'APIによる正規化データ操作', NOW()
)
RETURNING id;
```

## backend/src/app/entities/sql/workspace.sql

実行条件: このSQLの呼出し経路で実行

| 対象表 | CRUD | 参照・書込列 |
|---|---|---|
| recipeweave.workspace_revision | C,U | revision, user_id |

バインド変数: actor_id, row_id

```sql
-- 本人の変更を端末間の競合判定に反映し、業務更新と同時に版を増やす。
INSERT INTO recipeweave.workspace_revision AS current_revision (
    id, user_id, revision
)
VALUES (
    %(row_id)s, %(actor_id)s, 1
)
ON CONFLICT (user_id)
DO UPDATE SET revision = current_revision.revision + 1
RETURNING revision;
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
