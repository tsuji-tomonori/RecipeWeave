# 詳細設計: claim_shard

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/generation/shards/claim` — 生成範囲のリース取得

## 入力と処理前提

| 項目 | 仕様 |
|---|---|
| authentication | bearer |
| idempotency | フェンス・所有者・有効期限で条件付き更新する |
| transaction | リース変更と監査・outboxを同時確定する |
| effects | generation_shardのリースまたは進捗を更新する |

| 入力場所 | 名前 | 型 | 必須 |
|---|---|---|---|

### 本文: application/json

| 入力 | 型 | 必須 | 制約 | 意味 |
|---|---|---|---|---|
| lease_seconds | integer | 任意 | default=120; minimum=30.0; maximum=3600.0 | Lease Seconds |
| template_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | Template Id |

## データベースの対象と値の流れ

### `backend/src/app/apis/generation/claim_shard/sql/001_execute.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.generation_shard | RU | id: 不変ID; created_at: 作成日時; template_id: テンプレート版; start_ordinal: 開始序数; end_ordinal: 終了序数（排他的）; next_ordinal: 再開位置; lease_owner: ワーカー識別子; lease_expires_at: 有効期限; fence_token: 古い所有者の書込みを拒否; state: 待機/実行/完了/停止 |

対象条件: `WHERE s.id = selected.id`

行ロック: `FOR UPDATE SKIP LOCKED`

| SQLバインド | 実装上の値の出所 |
|---|---|
| lease_owner | service.identity.subject (backend/src/app/core/entity_generation.py:25) |
| lease_seconds | 型付きクエリの引数。呼出元のSQL仕様を参照。 |
| template_id | 型付きクエリの引数。呼出元のSQL仕様を参照。 |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| lease_owner | %(lease_owner)s |
| lease_expires_at | CURRENT_TIMESTAMP + MAKE_INTERVAL(secs =&gt; %(lease_seconds)s) |
| fence_token | s.fence_token + 1 |
| state | 'running' |

代入・選択式: `lease_owner = %(lease_owner)s; lease_expires_at = CURRENT_TIMESTAMP + MAKE_INTERVAL(secs => %(lease_seconds)s); fence_token = s.fence_token + 1; state = 'running'`

### `backend/src/app/entities/sql/audit.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.audit_event | C | id: 不変の行識別子; actor_id: 実行者（削除時匿名化）; action: publish/withdraw/erase等; entity_type: 対象テーブルの許可リスト; entity_key_hash: 対象識別子のハッシュ; reason: 理由（個人情報を含めない）; occurred_at: 時刻 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| action | 'update' (backend/src/app/core/entity_generation.py:38) / spec.action (backend/src/app/core/entity_service.py:142) |
| actor_id | self.identity.user_id (backend/src/app/core/entity_service.py:141) / self.identity.user_id (backend/src/app/core/entity_service.py:149) |
| entity_key_hash | key_hash (backend/src/app/core/entity_service.py:144) |
| entity_type | spec.table (backend/src/app/core/entity_service.py:143) |
| row_id | uuid4() (backend/src/app/core/entity_service.py:140) / uuid4() (backend/src/app/core/entity_service.py:149) / uuid4() (backend/src/app/core/entity_service.py:155) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(row_id)s |
| actor_id | %(actor_id)s |
| action | %(action)s |
| entity_type | %(entity_type)s |
| entity_key_hash | %(entity_key_hash)s |
| reason | 'APIによる正規化データ操作' |
| occurred_at | CURRENT_TIMESTAMP |

### `backend/src/app/entities/sql/outbox.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.outbox_event | C | id: 不変の行識別子; event_type: recipe_published/withdrawn/user_erased等; aggregate_id: 対象ID（配信対象でありFKでない）; payload: schema_version付き最小通知; attempt_count: 再試行数 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| aggregate_id | row_id (backend/src/app/core/entity_service.py:157) |
| event_type | f'{spec.table}.{spec.action}' (backend/src/app/core/entity_service.py:156) |
| row_id | uuid4() (backend/src/app/core/entity_service.py:140) / uuid4() (backend/src/app/core/entity_service.py:149) / uuid4() (backend/src/app/core/entity_service.py:155) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(row_id)s |
| event_type | %(event_type)s |
| aggregate_id | %(aggregate_id)s |
| payload | JSONB_BUILD_OBJECT('schema_version', 1, 'event_id', CAST(%(row_id)s AS TEXT), 'aggregate_id', CAST(%(aggregate_id)s AS TEXT), 'version', 1) |
| attempt_count | 0 |

### `backend/src/app/apis/auth/get_me/sql/q001_set_identity.sql`

実行条件: 認証依存の初期化時。同一主体の初回INSERTのみ作成し、既存行はDO NOTHING。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| role | identity.role (backend/src/app/core/identity.py:82) |
| user_id | str(identity.user_id) (backend/src/app/core/identity.py:82) / identity.user_id (backend/src/app/core/identity.py:83) / identity.user_id (backend/src/app/core/identity.py:86) / identity.user_id (backend/src/app/core/identity.py:89) / identity.user_id (backend/src/app/core/identity.py:96) |

代入・選択式: `SET_CONFIG('recipeweave.user_id', %(user_id)s, TRUE) AS user_setting; SET_CONFIG('recipeweave.role', %(role)s, TRUE) AS role_setting`

### `backend/src/app/apis/auth/get_me/sql/q002_initialize_user.sql`

実行条件: 認証依存の初期化時。同一主体の初回INSERTのみ作成し、既存行はDO NOTHING。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.app_user | C | id: 不変の行識別子; auth_subject: 認証基盤の不透明識別子; state: 利用/削除処理; locale: 表示言語; timezone: IANAタイムゾーン |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| subject | identity.subject (backend/src/app/core/identity.py:83) / identity.subject (backend/src/app/core/identity.py:86) |
| user_id | str(identity.user_id) (backend/src/app/core/identity.py:82) / identity.user_id (backend/src/app/core/identity.py:83) / identity.user_id (backend/src/app/core/identity.py:86) / identity.user_id (backend/src/app/core/identity.py:89) / identity.user_id (backend/src/app/core/identity.py:96) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(user_id)s |
| auth_subject | %(subject)s |
| state | 'active' |
| locale | 'ja' |
| timezone | 'Asia/Tokyo' |

競合時の処理: `ON CONFLICT(auth_subject) DO NOTHING`

### `backend/src/app/apis/auth/get_me/sql/q003_select_user.sql`

実行条件: 認証依存の初期化時。同一主体の初回INSERTのみ作成し、既存行はDO NOTHING。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.app_user | R | id: 不変の行識別子; auth_subject: 認証基盤の不透明識別子; state: 利用/削除処理 |

対象条件: `WHERE id = %(user_id)s AND auth_subject = %(subject)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| subject | identity.subject (backend/src/app/core/identity.py:83) / identity.subject (backend/src/app/core/identity.py:86) |
| user_id | str(identity.user_id) (backend/src/app/core/identity.py:82) / identity.user_id (backend/src/app/core/identity.py:83) / identity.user_id (backend/src/app/core/identity.py:86) / identity.user_id (backend/src/app/core/identity.py:89) / identity.user_id (backend/src/app/core/identity.py:96) |

代入・選択式: `id; state`

### `backend/src/app/apis/auth/get_me/sql/q004_initialize_revision.sql`

実行条件: 認証依存の初期化時。同一主体の初回INSERTのみ作成し、既存行はDO NOTHING。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.workspace_revision | C | id: 不変の行識別子; user_id: 所有者; revision: 全体のCAS版 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| row_id | uuid5(identity.user_id, 'workspace') (backend/src/app/core/identity.py:89) / uuid5(identity.user_id, 'kitchen:' + resource_code) (backend/src/app/core/identity.py:96) |
| user_id | str(identity.user_id) (backend/src/app/core/identity.py:82) / identity.user_id (backend/src/app/core/identity.py:83) / identity.user_id (backend/src/app/core/identity.py:86) / identity.user_id (backend/src/app/core/identity.py:89) / identity.user_id (backend/src/app/core/identity.py:96) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(row_id)s |
| user_id | %(user_id)s |
| revision | 0 |

競合時の処理: `ON CONFLICT(user_id) DO NOTHING`

### `backend/src/app/apis/auth/get_me/sql/q005_initialize_internal_resource.sql`

実行条件: 認証依存の初期化時。同一主体の初回INSERTのみ作成し、既存行はDO NOTHING。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.kitchen_resource | CR | id: 不変の行識別子; user_id: 所有者; resource_type_id: コンロ・鍋・人等; name: 左コンロ・26cmフライパン等; capacity: 容量; quantity: 同等資源数; active: 新規の調理計画で利用する資源か |
| recipeweave.resource_type | R | id: 不変の行識別子; code: burner/pan/person等; name: 道具名; status: 使用状態 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| resource_code | resource_code (backend/src/app/core/identity.py:96) |
| row_id | uuid5(identity.user_id, 'workspace') (backend/src/app/core/identity.py:89) / uuid5(identity.user_id, 'kitchen:' + resource_code) (backend/src/app/core/identity.py:96) |
| user_id | str(identity.user_id) (backend/src/app/core/identity.py:82) / identity.user_id (backend/src/app/core/identity.py:83) / identity.user_id (backend/src/app/core/identity.py:86) / identity.user_id (backend/src/app/core/identity.py:89) / identity.user_id (backend/src/app/core/identity.py:96) |

競合時の処理: `ON CONFLICT(id) DO NOTHING`

## 分岐・拒否条件

| 判定条件 | 例外・応答 | 定義元 |
|---|---|---|
| service.identity.role != 'admin' | HTTPException(status_code=403, detail='生成運用権限が必要です') | backend/src/app/core/entity_generation.py:17 |
| not rows | HTTPException(status_code=409, detail='取得対象がないか、リースが失効しました') | backend/src/app/core/entity_generation.py:17 |

## 出力

| 関数 | 返却式 | 定義元 |
|---|---|---|
| handle | execute(payload, EntityService(database, identity)) | backend/src/app/apis/generation/claim_shard/router.py:29 |
| execute | run_lease_operation(service, 'claim_shard', values) | backend/src/app/apis/generation/claim_shard/functions.py:9 |
| run_lease_operation | GenerationShardRow.model_validate(row) | backend/src/app/core/entity_generation.py:17 |

APIとして返す型・status・headerは [インターフェース](interface.md) の実OpenAPIを参照。

## 責務

| 関数 | 処理 | 定義元 |
|---|---|---|
| handle | 個別説明なし | backend/src/app/apis/generation/claim_shard/router.py:29 |
| execute | 生成範囲のリース取得の値を検証済み主体と固定SQLへ渡す。 | backend/src/app/apis/generation/claim_shard/functions.py:9 |
| run_lease_operation | 検証済みワーカーだけがリースを取得・更新でき、失効・交代後は409にする。 | backend/src/app/core/entity_generation.py:17 |
| EntityService.record_change | 本文を複製せず、行キーのハッシュと操作種別だけを監査へ残す。 | backend/src/app/core/entity_service.py:131 |

[SQL](queries.md) / [シーケンス](sequence.md) / [ログ](messages.md) / [要因別テスト](tests.md)
