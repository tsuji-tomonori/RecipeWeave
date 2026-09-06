# 詳細設計: entity_pantry_lot_create

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/entities/pantry_lot` — 手持ち食材ロットの作成

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
| amount | anyOf(number, string, null) | 任意 | anyOfの制約=number: minimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 残量 |
| edited | boolean | 必須 | 追加制約なし | 登録後の編集有無 |
| expires_on | anyOf(string (date), null) | 任意 | 追加制約なし | 表示期限 |
| form_id | string (uuid) | 必須 | 追加制約なし | 食材形態 |
| location | string | 必須 | minLength=1; maxLength=20000 | 冷蔵・冷凍・常温の保管場所 |
| opened_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 開封時点 |
| original_amount | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 登録時数量。不明はNULL |
| original_form_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 登録時の食材形態 |
| original_unit_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 登録時単位 |
| priority | string | 必須 | minLength=1; maxLength=20000 | 先に使う優先指定 |
| product_version_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 商品版 |
| quantity_quality | string | 必須 | minLength=1; maxLength=20000 | 数量の確定・不明 |
| source_import_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 登録元レシート |
| status | string | 必須 | minLength=1; maxLength=20000 | 在庫の有効・削除・レシート取消状態 |
| unit_id | string (uuid) | 必須 | 追加制約なし | 単位 |
| updated_at | string (date-time) | 必須 | 追加制約なし | 最終編集日時 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

## データベースの対象と値の流れ

### `backend/src/app/apis/entities/pantry_lot_create/sql/001_create.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.pantry_lot | C | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; form_id: 食材形態; product_version_id: 商品版; amount: 残量; unit_id: 単位; expires_on: 表示期限; opened_at: 開封時点; location: 冷蔵・冷凍・常温の保管場所; priority: 先に使う優先指定; status: 在庫の有効・削除・レシート取消状態; source_import_id: 登録元レシート; quantity_quality: 数量の確定・不明; original_form_id: 登録時の食材形態; original_amount: 登録時数量。不明はNULL; original_unit_id: 登録時単位; updated_at: 最終編集日時; edited: 登録後の編集有無 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| amount | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| edited | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| expires_on | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| form_id | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| location | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| opened_at | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| original_amount | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| original_form_id | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| original_unit_id | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| priority | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| product_version_id | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| quantity_quality | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| row_id | row_id or uuid4() (backend/src/app/core/entity_service.py:66) / uuid4() (backend/src/app/core/entity_service.py:140) / uuid4() (backend/src/app/core/entity_service.py:149) / uuid4() (backend/src/app/core/entity_service.py:155) |
| source_import_id | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| status | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| unit_id | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| updated_at | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |
| user_id | 検証済みリクエストモデル → payload → values → params。共有サービスがJSONB/整数列を変換する。 |

### `backend/src/app/apis/entities/pantry_lot_create/sql/002_reference_user_id.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.app_user | R | id: 不変の行識別子 |

対象条件: `WHERE t.id = %(reference_id)s AND t.id = %(actor_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/entity_service.py:67) / self.identity.user_id (backend/src/app/core/entity_service.py:87) / self.identity.user_id (backend/src/app/core/entity_service.py:141) / self.identity.user_id (backend/src/app/core/entity_service.py:149) |
| reference_id | value (backend/src/app/core/entity_service.py:86) |

代入・選択式: `t.id`

### `backend/src/app/apis/entities/pantry_lot_create/sql/003_reference_source_import_id.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.receipt_import | R | id: 不変の行識別子; user_id: 所有者 |

対象条件: `WHERE t.id = %(reference_id)s AND t.user_id = %(actor_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/entity_service.py:67) / self.identity.user_id (backend/src/app/core/entity_service.py:87) / self.identity.user_id (backend/src/app/core/entity_service.py:141) / self.identity.user_id (backend/src/app/core/entity_service.py:149) |
| reference_id | value (backend/src/app/core/entity_service.py:86) |

代入・選択式: `t.id`

### `backend/src/app/entities/sql/audit.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.audit_event | C | id: 不変の行識別子; actor_id: 実行者（削除時匿名化）; action: publish/withdraw/erase等; entity_type: 対象テーブルの許可リスト; entity_key_hash: 対象識別子のハッシュ; reason: 理由（個人情報を含めない）; occurred_at: 時刻 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| action | spec.action (backend/src/app/core/entity_service.py:111) / spec.action (backend/src/app/core/entity_service.py:142) |
| actor_id | self.identity.user_id (backend/src/app/core/entity_service.py:67) / self.identity.user_id (backend/src/app/core/entity_service.py:87) / self.identity.user_id (backend/src/app/core/entity_service.py:141) / self.identity.user_id (backend/src/app/core/entity_service.py:149) |
| entity_key_hash | key_hash (backend/src/app/core/entity_service.py:144) |
| entity_type | spec.table (backend/src/app/core/entity_service.py:143) |
| row_id | row_id or uuid4() (backend/src/app/core/entity_service.py:66) / uuid4() (backend/src/app/core/entity_service.py:140) / uuid4() (backend/src/app/core/entity_service.py:149) / uuid4() (backend/src/app/core/entity_service.py:155) |

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

### `backend/src/app/entities/sql/workspace.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.workspace_revision | CU | user_id: 所有者; revision: 全体のCAS版 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| actor_id | self.identity.user_id (backend/src/app/core/entity_service.py:67) / self.identity.user_id (backend/src/app/core/entity_service.py:87) / self.identity.user_id (backend/src/app/core/entity_service.py:141) / self.identity.user_id (backend/src/app/core/entity_service.py:149) |
| row_id | row_id or uuid4() (backend/src/app/core/entity_service.py:66) / uuid4() (backend/src/app/core/entity_service.py:140) / uuid4() (backend/src/app/core/entity_service.py:149) / uuid4() (backend/src/app/core/entity_service.py:155) |

競合時の処理: `ON CONFLICT(user_id) DO UPDATE SET revision = current_revision.revision + 1`

| 既存行の更新列 | 競合時に設定する式 |
|---|---|
| revision | current_revision.revision + 1 |

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
| value is None | HTTPException(status_code=428, detail='If-Matchが必要です') | backend/src/app/core/entity_service.py:23 |
| re.fullmatch('"[0-9]+"', value) is None | HTTPException(status_code=422, detail='If-Matchの形式が不正です') | backend/src/app/core/entity_service.py:23 |
| not spec.owned and self.identity.role != 'admin' | HTTPException(status_code=403, detail='管理者権限が必要です') | backend/src/app/core/entity_service.py:39 |
| not 1 &lt;= limit &lt;= 100 | HTTPException(status_code=422, detail='取得件数は1から100です') | backend/src/app/core/entity_service.py:39 |
| set(values) != set(spec.input_columns) | HTTPException(status_code=422, detail='入力項目が操作契約と一致しません') | backend/src/app/core/entity_service.py:39 |
| spec.table == 'app_user' and values.get('auth_subject', self.identity.subject) != self.identity.subject | HTTPException(status_code=403, detail='認証主体は変更できません') | backend/src/app/core/entity_service.py:39 |
| 'user_id' in values and str(values['user_id']) != str(self.identity.user_id) | HTTPException(status_code=403, detail='別の利用者を指定できません') | backend/src/app/core/entity_service.py:39 |
| not rows and spec.action in {'get', 'update', 'delete'} | HTTPException(status_code=status, detail='対象がないか行の版が変わりました') | backend/src/app/core/entity_service.py:39 |
| value is not None and (not query(self.connection, {'reference_id': value, 'actor_id': self.identity.user_id, 'preview': catalog_preview_enabled()})) | HTTPException(status_code=403, detail='参照先を利用できません') | backend/src/app/core/entity_service.py:39 |

## 出力

| 関数 | 返却式 | 定義元 |
|---|---|---|
| handle | result | backend/src/app/apis/entities/pantry_lot_create/router.py:28 |
| execute | PantryLotRow.model_validate(rows[0]) | backend/src/app/apis/entities/pantry_lot_create/functions.py:7 |
| parse_etag | value[1:-1] | backend/src/app/core/entity_service.py:23 |
| EntityService.execute | rows | backend/src/app/core/entity_service.py:39 |

APIとして返す型・status・headerは [インターフェース](interface.md) の実OpenAPIを参照。

## 責務

| 関数 | 処理 | 定義元 |
|---|---|---|
| handle | 手持ち食材ロットの作成。認証情報は依存から取得し、本人所有または管理者権限を検査する。 | backend/src/app/apis/entities/pantry_lot_create/router.py:28 |
| execute | 手持ち食材ロットの作成を固定操作契約で実行し、DB行を専用応答型へ検証する。 | backend/src/app/apis/entities/pantry_lot_create/functions.py:7 |
| parse_etag | ワイルドカードや複数指定を拒否し、読取り時の行版を必須にする。 | backend/src/app/core/entity_service.py:23 |
| EntityService.execute | 本人の行を絞り込み、更新前の版と親所有権を検証して実行する。 | backend/src/app/core/entity_service.py:39 |
| EntityService.record_change | 本文を複製せず、行キーのハッシュと操作種別だけを監査へ残す。 | backend/src/app/core/entity_service.py:131 |

[SQL](queries.md) / [シーケンス](sequence.md) / [ログ](messages.md) / [要因別テスト](tests.md)
