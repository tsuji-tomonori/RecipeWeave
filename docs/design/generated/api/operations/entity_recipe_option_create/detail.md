# 詳細設計: entity_recipe_option_create

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/entities/recipe_option` — 版の分類・特徴の作成

## 入力と処理前提

| 項目 | 仕様 |
|---|---|
| authentication | bearer |
| idempotency | GETは副作用なし。POSTは新規IDを採番する。 |
| transaction | 本人所有権・参照・DB制約・監査・outboxを同じトランザクションで検査する |
| effects | 正規化行の変更。監査を追記しカタログ変更はoutboxへ通知する。 |

| 入力場所 | 名前 | 型 | 必須 |
|---|---|---|---|

### 本文: application/json

| 入力 | 型 | 必須 | 制約 | 意味 |
|---|---|---|---|---|
| option_id | string (uuid) | 必須 | 追加制約なし | 特徴値 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 対象版 |

## データベースの対象と値の流れ

### `backend/src/app/apis/entities/recipe_option_create/sql/001_create.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.recipe_option | C | id: 不変の行識別子; created_at: 作成日時（UTC）; recipe_version_id: 対象版; option_id: 特徴値 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| option_id | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| recipe_version_id | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| row_id | row_id or uuid4() (backend/src/app/core/entity_service.py:65) / uuid4() (backend/src/app/core/entity_service.py:139) / uuid4() (backend/src/app/core/entity_service.py:148) / uuid4() (backend/src/app/core/entity_service.py:154) |

### `backend/src/app/entities/sql/audit.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.audit_event | C | id: 不変の行識別子; actor_id: 実行者（削除時匿名化）; action: publish/withdraw/erase等; entity_type: 対象テーブルの許可リスト; entity_key_hash: 対象識別子のハッシュ; reason: 理由（個人情報を含めない）; occurred_at: 時刻 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| action | spec.action (backend/src/app/core/entity_service.py:110) / spec.action (backend/src/app/core/entity_service.py:141) |
| actor_id | self.identity.user_id (backend/src/app/core/entity_service.py:66) / self.identity.user_id (backend/src/app/core/entity_service.py:86) / self.identity.user_id (backend/src/app/core/entity_service.py:140) / self.identity.user_id (backend/src/app/core/entity_service.py:148) |
| entity_key_hash | key_hash (backend/src/app/core/entity_service.py:143) |
| entity_type | spec.table (backend/src/app/core/entity_service.py:142) |
| row_id | row_id or uuid4() (backend/src/app/core/entity_service.py:65) / uuid4() (backend/src/app/core/entity_service.py:139) / uuid4() (backend/src/app/core/entity_service.py:148) / uuid4() (backend/src/app/core/entity_service.py:154) |

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
| aggregate_id | row_id (backend/src/app/core/entity_service.py:156) |
| event_type | f'{spec.table}.{spec.action}' (backend/src/app/core/entity_service.py:155) |
| row_id | row_id or uuid4() (backend/src/app/core/entity_service.py:65) / uuid4() (backend/src/app/core/entity_service.py:139) / uuid4() (backend/src/app/core/entity_service.py:148) / uuid4() (backend/src/app/core/entity_service.py:154) |

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
| value is None | HTTPException(status_code=428, detail='If-Matchが必要です') | backend/src/app/core/entity_service.py:22 |
| re.fullmatch('"[0-9]+"', value) is None | HTTPException(status_code=422, detail='If-Matchの形式が不正です') | backend/src/app/core/entity_service.py:22 |
| not spec.owned and self.identity.role != 'admin' | HTTPException(status_code=403, detail='管理者権限が必要です') | backend/src/app/core/entity_service.py:38 |
| not 1 &lt;= limit &lt;= 100 | HTTPException(status_code=422, detail='取得件数は1から100です') | backend/src/app/core/entity_service.py:38 |
| set(values) != set(spec.input_columns) | HTTPException(status_code=422, detail='入力項目が操作契約と一致しません') | backend/src/app/core/entity_service.py:38 |
| spec.table == 'app_user' and values.get('auth_subject', self.identity.subject) != self.identity.subject | HTTPException(status_code=403, detail='認証主体は変更できません') | backend/src/app/core/entity_service.py:38 |
| 'user_id' in values and str(values['user_id']) != str(self.identity.user_id) | HTTPException(status_code=403, detail='別の利用者を指定できません') | backend/src/app/core/entity_service.py:38 |
| not rows and spec.action in {'get', 'update', 'delete'} | HTTPException(status_code=status, detail='対象がないか行の版が変わりました') | backend/src/app/core/entity_service.py:38 |
| value is not None and (not query(self.connection, {'reference_id': value, 'actor_id': self.identity.user_id, 'preview': local_auth_enabled()})) | HTTPException(status_code=403, detail='参照先を利用できません') | backend/src/app/core/entity_service.py:38 |

## 出力

| 関数 | 返却式 | 定義元 |
|---|---|---|
| handle | result | backend/src/app/apis/entities/recipe_option_create/router.py:28 |
| execute | RecipeOptionRow.model_validate(rows[0]) | backend/src/app/apis/entities/recipe_option_create/functions.py:7 |
| parse_etag | value[1:-1] | backend/src/app/core/entity_service.py:22 |
| EntityService.execute | rows | backend/src/app/core/entity_service.py:38 |

APIとして返す型・status・headerは [インターフェース](interface.md) の実OpenAPIを参照。

## 責務

| 関数 | 処理 | 定義元 |
|---|---|---|
| handle | 版の分類・特徴の作成。認証情報は依存から取得し、本人所有または管理者権限を検査する。 | backend/src/app/apis/entities/recipe_option_create/router.py:28 |
| execute | 版の分類・特徴の作成を固定操作契約で実行し、DB行を専用応答型へ検証する。 | backend/src/app/apis/entities/recipe_option_create/functions.py:7 |
| parse_etag | ワイルドカードや複数指定を拒否し、読取り時の行版を必須にする。 | backend/src/app/core/entity_service.py:22 |
| EntityService.execute | 本人の行を絞り込み、更新前の版と親所有権を検証して実行する。 | backend/src/app/core/entity_service.py:38 |
| EntityService.record_change | 本文を複製せず、行キーのハッシュと操作種別だけを監査へ残す。 | backend/src/app/core/entity_service.py:130 |

[SQL](queries.md) / [シーケンス](sequence.md) / [ログ](messages.md) / [要因別テスト](tests.md)
