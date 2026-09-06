# 詳細設計: unsave_recipe

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`DELETE /api/saved-recipes/{row_id}` — 料理の保存を解除する

## 入力と処理前提

| 項目 | 仕様 |
|---|---|
| authentication | 検証済みBearerトークンと本人所有権 |
| idempotency | 要求のexpectedVersionで再送・同時更新を検出する |
| transaction | 本人のworkspace_revisionをロックし、各正規化行・監査・版を原子的に確定する |
| effects | 正規化された本人の業務データを更新する |

| 入力場所 | 名前 | 型 | 必須 |
|---|---|---|---|
| path | row_id | string (uuid) | True |

### 本文: application/json

| 入力 | 型 | 必須 | 制約 | 意味 |
|---|---|---|---|---|
| expectedVersion | integer | 必須 | minimum=0.0; maximum=9007199254740990.0 | Expectedversion |

## データベースの対象と値の流れ

### `backend/src/app/apis/workspace/unsave_recipe/sql/q001_recipe.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.recipe | R | id: 不変の行識別子; status: 公開状態 |
| recipeweave.recipe_version | R | id: 不変の行識別子; recipe_id: 所属レシピ; version: 版番号; status: 版の状態; validation: 公開審査 |

対象条件: `WHERE r.id = %(recipe_id)s AND ((rv.status = 'published' AND r.status = 'published' AND rv.validation = 'passed') OR (%(preview)s AND rv.status = 'draft' AND r.status = 'draft'))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| preview | catalog_preview_enabled() (backend/src/app/core/workspace_service.py:330) |
| recipe_id | row_id (backend/src/app/core/workspace_service.py:330) |

代入・選択式: `rv.id`

### `backend/src/app/apis/workspace/unsave_recipe/sql/q002_event.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.user_recipe_event | C | id: 不変の行識別子; user_id: 利用者; recipe_version_id: 提案版; kind: 提示/調理/評価; occurred_at: 発生時刻; request_key: リクエスト識別子 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| request_key | f'{name}:{request.expected_version}:{row_id}' (backend/src/app/core/workspace_service.py:333) |
| row_id | uuid4() (backend/src/app/core/workspace_service.py:72) / uuid4() (backend/src/app/core/workspace_service.py:333) |
| user_id | self.user_id (backend/src/app/core/workspace_service.py:65) / self.user_id (backend/src/app/core/workspace_service.py:71) / self.user_id (backend/src/app/core/workspace_service.py:72) / self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) / self.user_id (backend/src/app/core/workspace_service.py:333) |
| version_id | rows[0]['id'] (backend/src/app/core/workspace_service.py:333) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(row_id)s |
| user_id | %(user_id)s |
| recipe_version_id | %(version_id)s |
| kind | 'disliked' |
| occurred_at | CLOCK_TIMESTAMP() |
| request_key | %(request_key)s |

### `backend/src/app/apis/workspace/unsave_recipe/sql/q900_lock_revision.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.workspace_revision | R | user_id: 所有者; revision: 全体のCAS版 |

対象条件: `WHERE user_id = %(user_id)s`

行ロック: `FOR UPDATE`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:65) / self.user_id (backend/src/app/core/workspace_service.py:71) / self.user_id (backend/src/app/core/workspace_service.py:72) / self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) / self.user_id (backend/src/app/core/workspace_service.py:333) |

代入・選択式: `revision`

### `backend/src/app/apis/workspace/unsave_recipe/sql/q901_advance_revision.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.workspace_revision | U | user_id: 所有者; revision: 全体のCAS版 |

対象条件: `WHERE user_id = %(user_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:65) / self.user_id (backend/src/app/core/workspace_service.py:71) / self.user_id (backend/src/app/core/workspace_service.py:72) / self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) / self.user_id (backend/src/app/core/workspace_service.py:333) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| revision | revision + 1 |

代入・選択式: `revision = revision + 1`

### `backend/src/app/apis/workspace/unsave_recipe/sql/q902_append_audit.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.audit_event | C | id: 不変の行識別子; actor_id: 実行者（削除時匿名化）; action: publish/withdraw/erase等; entity_type: 対象テーブルの許可リスト; entity_key_hash: 対象識別子のハッシュ; reason: 理由（個人情報を含めない）; occurred_at: 時刻 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| action | queries.operation (backend/src/app/core/workspace_service.py:72) |
| key_hash | hashlib.sha256(str(self.user_id).encode()).hexdigest() (backend/src/app/core/workspace_service.py:72) |
| row_id | uuid4() (backend/src/app/core/workspace_service.py:72) / uuid4() (backend/src/app/core/workspace_service.py:333) |
| user_id | self.user_id (backend/src/app/core/workspace_service.py:65) / self.user_id (backend/src/app/core/workspace_service.py:71) / self.user_id (backend/src/app/core/workspace_service.py:72) / self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) / self.user_id (backend/src/app/core/workspace_service.py:333) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(row_id)s |
| actor_id | %(user_id)s |
| action | %(action)s |
| entity_type | 'workspace' |
| entity_key_hash | %(key_hash)s |
| reason | '本人の業務操作' |
| occurred_at | CURRENT_TIMESTAMP |

### `backend/src/app/apis/workspace/get_workspace/sql/q001_revision.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.workspace_revision | R | user_id: 所有者; revision: 全体のCAS版 |

対象条件: `WHERE user_id = %(user_id)s`

行ロック: `FOR SHARE`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:65) / self.user_id (backend/src/app/core/workspace_service.py:71) / self.user_id (backend/src/app/core/workspace_service.py:72) / self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) / self.user_id (backend/src/app/core/workspace_service.py:333) |

代入・選択式: `revision`

### `backend/src/app/apis/workspace/get_workspace/sql/q002_lots.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food_form | R | id: 不変の行識別子; food_id: 対応食材; name: 生皮付き・冷凍刻み等 |
| recipeweave.pantry_lot | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; form_id: 食材形態; amount: 残量; unit_id: 単位; expires_on: 表示期限; location: 冷蔵・冷凍・常温の保管場所; priority: 先に使う優先指定; status: 在庫の有効・削除・レシート取消状態; source_import_id: 登録元レシート; original_form_id: 登録時の食材形態; original_amount: 登録時数量。不明はNULL; original_unit_id: 登録時単位; updated_at: 最終編集日時; edited: 登録後の編集有無 |
| recipeweave.unit | R | id: 不変の行識別子; code: 単位コード |

対象条件: `WHERE p.user_id = %(user_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:65) / self.user_id (backend/src/app/core/workspace_service.py:71) / self.user_id (backend/src/app/core/workspace_service.py:72) / self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) / self.user_id (backend/src/app/core/workspace_service.py:333) |

代入・選択式: `p.id; f.food_id; f.name AS form; p.amount; u.code AS unit; p.original_amount; p.location; p.priority; p.expires_on; p.created_at; p.updated_at; p.source_import_id; p.status; p.edited; COALESCE(ofm.food_id, f.food_id) AS original_food_id; COALESCE(ou.code, u.code) AS original_unit`

### `backend/src/app/apis/workspace/get_workspace/sql/q003_consumption.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.pantry_consumption | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; session_id: 消費した調理セッション; lot_id: 消費元ロット; amount: 消費数量; unit_id: 消費数量の単位 |
| recipeweave.unit | R | id: 不変の行識別子; code: 単位コード |

対象条件: `WHERE c.user_id = %(user_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:65) / self.user_id (backend/src/app/core/workspace_service.py:71) / self.user_id (backend/src/app/core/workspace_service.py:72) / self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) / self.user_id (backend/src/app/core/workspace_service.py:333) |

代入・選択式: `c.lot_id; c.amount; u.code AS unit; c.session_id`

### `backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.receipt_import | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; file_sha256: 画像本文のSHA256。本文はDBに保存しない; idempotency_key: 本人内で一意の再送防止キー; status: draft/committed/revertedの状態; reverted_at: 登録取消日時 |

対象条件: `WHERE r.user_id = %(user_id)s AND r.status IN ('committed', 'reverted')`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:65) / self.user_id (backend/src/app/core/workspace_service.py:71) / self.user_id (backend/src/app/core/workspace_service.py:72) / self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) / self.user_id (backend/src/app/core/workspace_service.py:333) |

代入・選択式: `r.id; r.file_sha256; r.idempotency_key; r.created_at; r.status; r.reverted_at`

### `backend/src/app/apis/workspace/get_workspace/sql/q005_menu.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者; revision: 楽観ロック版 |
| recipeweave.menu_item | R | id: 不変の行識別子; menu_id: 献立; recipe_version_id: 固定レシピ版; servings: その料理を作る人数; position: 表示順 |
| recipeweave.recipe_version | R | id: 不変の行識別子; recipe_id: 所属レシピ |

対象条件: `WHERE m.id = %(menu_id)s AND m.user_id = %(user_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| menu_id | menu_id (backend/src/app/core/workspace_service.py:188) / menu_id (backend/src/app/core/workspace_service.py:206) |
| user_id | self.user_id (backend/src/app/core/workspace_service.py:65) / self.user_id (backend/src/app/core/workspace_service.py:71) / self.user_id (backend/src/app/core/workspace_service.py:72) / self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) / self.user_id (backend/src/app/core/workspace_service.py:333) |

代入・選択式: `mi.id; rv.recipe_id; mi.servings; mi.recipe_version_id; m.revision`

### `backend/src/app/apis/workspace/get_workspace/sql/q006_ingredients.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food_form | R | id: 不変の行識別子; food_id: 対応食材; name: 生皮付き・冷凍刻み等 |
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者 |
| recipeweave.menu_ingredient_override | R | id: 不変の行識別子; menu_item_id: 対象料理; ingredient_line_id: 元材料行; selected: 任意材料を使うか; amount: 適量等の確定基準量 |
| recipeweave.menu_item | R | id: 不変の行識別子; menu_id: 献立; recipe_version_id: 固定レシピ版; servings: その料理を作る人数; position: 表示順 |
| recipeweave.recipe_ingredient | R | id: 不変の行識別子; recipe_version_id: 親版; line_no: 表示順; form_id: 使用形態; amount: 確定値または範囲下限; unit_id: 登録単位 |
| recipeweave.recipe_version | R | id: 不変の行識別子; base_servings: 登録分量が何人前か |
| recipeweave.unit | R | id: 不変の行識別子; code: 単位コード |

対象条件: `WHERE m.id = %(menu_id)s AND m.user_id = %(user_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| menu_id | menu_id (backend/src/app/core/workspace_service.py:188) / menu_id (backend/src/app/core/workspace_service.py:206) |
| user_id | self.user_id (backend/src/app/core/workspace_service.py:65) / self.user_id (backend/src/app/core/workspace_service.py:71) / self.user_id (backend/src/app/core/workspace_service.py:72) / self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) / self.user_id (backend/src/app/core/workspace_service.py:333) |

代入・選択式: `mi.id AS menu_item_id; f.food_id; f.name AS form; ri.id AS ingredient_id; u.code AS unit; ov.id AS override_id; CASE WHEN ov.selected = FALSE THEN 0 ELSE ov.amount END AS override_amount; ri.amount * mi.servings / rv.base_servings AS scaled_amount`

### `backend/src/app/apis/workspace/get_workspace/sql/q007_saved.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.recipe_version | R | id: 不変の行識別子; recipe_id: 所属レシピ |
| recipeweave.user_recipe_event | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 利用者; recipe_version_id: 提案版; kind: 提示/調理/評価; occurred_at: 発生時刻 |

対象条件: `WHERE ranked.rank = 1 AND ranked.kind = 'liked'`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:65) / self.user_id (backend/src/app/core/workspace_service.py:71) / self.user_id (backend/src/app/core/workspace_service.py:72) / self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) / self.user_id (backend/src/app/core/workspace_service.py:333) |

代入・選択式: `ranked.recipe_id`

### `backend/src/app/apis/workspace/get_workspace/sql/q008_settings.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.kitchen_resource | R | user_id: 所有者; resource_type_id: コンロ・鍋・人等; active: 新規の調理計画で利用する資源か |
| recipeweave.resource_type | R | id: 不変の行識別子; code: burner/pan/person等; name: 道具名 |
| recipeweave.user_exclusion | R | user_id: 利用者; food_id: 食材 |
| recipeweave.user_pantry_food | R | user_id: 所有者; food_id: 常備食材 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:65) / self.user_id (backend/src/app/core/workspace_service.py:71) / self.user_id (backend/src/app/core/workspace_service.py:72) / self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) / self.user_id (backend/src/app/core/workspace_service.py:333) |

代入・選択式: `settings.kind; settings.setting_value`

### `backend/src/app/apis/workspace/get_workspace/sql/q009_custom_foods.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food | R | id: 不変の行識別子; name: 食材名・加工品種別 |
| recipeweave.food_form | R | food_id: 対応食材; base_unit_id: 計算基準単位 |
| recipeweave.unit | R | id: 不変の行識別子; code: 単位コード |
| recipeweave.user_food | R | user_id: 所有者; food_id: 独自食材 |

対象条件: `WHERE uf.user_id = %(user_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:65) / self.user_id (backend/src/app/core/workspace_service.py:71) / self.user_id (backend/src/app/core/workspace_service.py:72) / self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) / self.user_id (backend/src/app/core/workspace_service.py:333) |

代入・選択式: `f.id; f.name; u.code AS unit`

### `backend/src/app/apis/workspace/get_workspace/sql/q010_shopping.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.unit | R | id: 不変の行識別子; code: 単位コード |
| recipeweave.user_shopping_check | R | id: 不変の行識別子; user_id: 所有者; key: 買い物対象の安定キー; signature: 数量・商品条件の一致確認用署名; food_id: 対象食材; amount: 必要数量。不明はNULL; unit_id: 数量単位; checked_at: 購入確認日時; archived: 保管済みか |

対象条件: `WHERE c.user_id = %(user_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:65) / self.user_id (backend/src/app/core/workspace_service.py:71) / self.user_id (backend/src/app/core/workspace_service.py:72) / self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) / self.user_id (backend/src/app/core/workspace_service.py:333) |

代入・選択式: `c.key AS client_key; c.signature; c.food_id; c.amount; u.code AS unit; c.checked_at; c.archived`

### `backend/src/app/apis/workspace/get_workspace/sql/q011_session.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.cooking_session | R | id: 不変の行識別子; created_at: 作成日時（UTC）; menu_id: 対象献立; status: 実行状態; input_snapshot: 材料・資源・人数の固定入力; current_task_index: 調理画面の現在の工程位置（0始まり） |
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者 |

対象条件: `WHERE m.user_id = %(user_id)s AND s.status <> 'cancelled'`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/workspace_service.py:65) / self.user_id (backend/src/app/core/workspace_service.py:71) / self.user_id (backend/src/app/core/workspace_service.py:72) / self.user_id (backend/src/app/core/workspace_service.py:84) / self.user_id (backend/src/app/core/workspace_service.py:85) / self.user_id (backend/src/app/core/workspace_service.py:133) / self.user_id (backend/src/app/core/workspace_service.py:106) / self.user_id (backend/src/app/core/workspace_service.py:120) / self.user_id (backend/src/app/core/workspace_service.py:148) / self.user_id (backend/src/app/core/workspace_service.py:159) / self.user_id (backend/src/app/core/workspace_service.py:172) / self.user_id (backend/src/app/core/workspace_service.py:188) / self.user_id (backend/src/app/core/workspace_service.py:206) / self.user_id (backend/src/app/core/workspace_service.py:333) |

代入・選択式: `s.id; s.menu_id; s.status; s.current_task_index; s.input_snapshot`

### `backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu_item | R | id: 不変の行識別子; recipe_version_id: 固定レシピ版; position: 表示順 |
| recipeweave.recipe | R | id: 不変の行識別子; title: 代表名 |
| recipeweave.recipe_step | R | id: 不変の行識別子; step_no: 表示順（依存順とは別）; instruction: 個別補足; attention: 作業者拘束; duration_max_s: 所要秒上限; scaling_rule_id: 時間の人数変更規則; title: 工程の短い見出し |
| recipeweave.recipe_version | R | id: 不変の行識別子; recipe_id: 所属レシピ |
| recipeweave.scaling_rule | R | id: 不変の行識別子; mode: 比例・バッチ等 |
| recipeweave.session_task | R | id: 不変の行識別子; session_id: 実行; menu_item_id: 料理; step_id: 元工程; planned_start_s: 開始相対秒; planned_end_s: 終了相対秒; status: 進捗; timer_started_at: 稼働中タイマーの開始日時; timer_duration_s: 利用者が設定したタイマー秒数; duration_source: 計画時間の根拠。料理の時間規則または利用者が確認した見積り; confirmed_duration_s: 利用者が確認した工程の見積り秒数。実測値ではなく、計画後は変更しない |

対象条件: `WHERE t.session_id = %(session_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| session_id | 型付きクエリの引数。呼出元のSQL仕様を参照。 |

代入・選択式: `t.id; t.menu_item_id; t.step_id; t.planned_start_s; t.planned_end_s; t.duration_source; t.confirmed_duration_s; t.status; t.timer_started_at; t.timer_duration_s; rv.recipe_id; r.title AS recipe_name; st.title; st.instruction; st.attention; st.duration_max_s; scaling.mode AS scaling_mode`

### `backend/src/app/apis/workspace/get_workspace/sql/q013_task_resources.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.resource_type | R | id: 不変の行識別子; code: burner/pan/person等; name: 道具名 |
| recipeweave.session_task | R | id: 不変の行識別子; session_id: 実行; step_id: 元工程 |
| recipeweave.step_resource | R | step_id: 対象工程; resource_type_id: 要求種別 |

対象条件: `WHERE t.session_id = %(session_id)s AND r.code <> 'person'`

| SQLバインド | 実装上の値の出所 |
|---|---|
| session_id | 型付きクエリの引数。呼出元のSQL仕様を参照。 |

代入・選択式: `t.id AS task_id; r.name`

### `backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food_form | R | id: 不変の行識別子; food_id: 対応食材; name: 生皮付き・冷凍刻み等 |
| recipeweave.ingredient_total | R | id: 不変の行識別子; session_id: 固定計算対象; form_id: 合算可能な形態; product_version_id: 商品固定; unit_id: 基準単位; required_amount: 必要量; actual_amount: 利用者が確定した実使用量。不明はNULL; consumption_outcome: 未要求・反映済み・在庫不足・数量不明・単位不一致の結果 |
| recipeweave.pantry_consumption | R | id: 不変の行識別子; created_at: 作成日時（UTC）; session_id: 消費した調理セッション; lot_id: 消費元ロット; amount: 消費数量 |
| recipeweave.pantry_lot | R | id: 不変の行識別子; form_id: 食材形態; product_version_id: 商品版; unit_id: 単位 |
| recipeweave.unit | R | id: 不変の行識別子; code: 単位コード |

対象条件: `WHERE total.session_id = %(session_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| session_id | 型付きクエリの引数。呼出元のSQL仕様を参照。 |

代入・選択式: `total.id; fm.food_id; fm.name AS form; total.required_amount; total.actual_amount; total.consumption_outcome; u.code AS unit; COALESCE(SUM(c.amount), 0) AS consumed_amount; ARRAY_AGG(c.lot_id ORDER BY c.created_at, c.id) FILTER(WHERE c.id IS NOT NULL) AS lot_ids`

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
| not rows or int(rows[0]['revision']) != request.expected_version | HTTPException(409, '他の画面で更新されています。最新の内容を読み込んでください') | backend/src/app/core/workspace_service.py:63 |
| not rows | HTTPException(404, '料理が公開されていません') | backend/src/app/core/workspace_service.py:328 |

## 出力

| 関数 | 返却式 | 定義元 |
|---|---|---|
| handle | execute(WorkspaceService(database, identity), request, row_id) | backend/src/app/apis/workspace/unsave_recipe/router.py:24 |
| execute | service.unsave_recipe(request, row_id) | backend/src/app/apis/workspace/unsave_recipe/functions.py:8 |
| quantity | {'value': None if value is None else float(value), 'unit': unit} | backend/src/app/core/workspace_service.py:41 |
| iso | value.isoformat() if isinstance(value, date &#124; datetime) else None | backend/src/app/core/workspace_service.py:46 |
| WorkspaceService.queries | OperationQueries(self.connection, 'workspace/' + name) | backend/src/app/core/workspace_service.py:60 |
| WorkspaceService.begin | queries | backend/src/app/core/workspace_service.py:63 |
| WorkspaceService.finish | self.get_workspace() | backend/src/app/core/workspace_service.py:70 |
| WorkspaceService.get_workspace | AppSnapshot.model_validate({'schemaVersion': 1, 'version': int(revision[0]['revision']) if revision else 0, 'lots': lots, 'imports': imports, 'drafts': {}, 'meal': meal, 'saved': [str(r['recipe_id']) for r in q.run('q007_saved', user_id=self.user_id)], 'shoppingChecks': checks, 'cooking': cooking, 'settings': settings, 'customFoods': customs, 'search': {'selectedFoodIds': [], 'match': 'all', 'maxMinutes': None, 'noShopping': False, 'equipment': []}}) | backend/src/app/core/workspace_service.py:81 |
| WorkspaceService.read_meal | [{'id': str(r['id']), 'recipeId': str(r['recipe_id']), 'recipeVersionId': str(r['recipe_version_id']), 'servings': float(r['servings']), 'adjusted': any((a['override_id'] is not None for a in amounts if a['menu_item_id'] == r['id'])), 'amounts': {str(a['ingredient_id']): quantity(a['override_amount'] if a['override_id'] else a['scaled_amount'], a['unit']) for a in amounts if a['menu_item_id'] == r['id']}} for r in q.run('q005_menu', menu_id=menu_id, user_id=self.user_id)] | backend/src/app/core/workspace_service.py:187 |
| WorkspaceService._save_recipe | self.finish(q) | backend/src/app/core/workspace_service.py:328 |
| WorkspaceService.unsave_recipe | self._save_recipe('unsave_recipe', request, row_id) | backend/src/app/core/workspace_service.py:346 |

APIとして返す型・status・headerは [インターフェース](interface.md) の実OpenAPIを参照。

## 責務

| 関数 | 処理 | 定義元 |
|---|---|---|
| handle | 料理の保存を解除する。呼出元が送った利用者IDは使用しない。 | backend/src/app/apis/workspace/unsave_recipe/router.py:24 |
| execute | 料理の保存を解除する。永続値は業務サービスが検証し、同一トランザクションで扱う。 | backend/src/app/apis/workspace/unsave_recipe/functions.py:8 |
| quantity | 未知の数量をNULLのまま通信し、DBの十進値を表示用の数へ変換する。 | backend/src/app/core/workspace_service.py:41 |
| iso | 日時はISO形式にそろえる。 | backend/src/app/core/workspace_service.py:46 |
| WorkspaceService.queries | 個別説明なし | backend/src/app/core/workspace_service.py:60 |
| WorkspaceService.begin | 個別説明なし | backend/src/app/core/workspace_service.py:63 |
| WorkspaceService.finish | 個別説明なし | backend/src/app/core/workspace_service.py:70 |
| WorkspaceService.get_workspace | 在庫・献立・設定・履歴を各テーブルから集約し、一貫した版を返す。 | backend/src/app/core/workspace_service.py:81 |
| WorkspaceService.read_meal | 個別説明なし | backend/src/app/core/workspace_service.py:187 |
| WorkspaceService._save_recipe | 個別説明なし | backend/src/app/core/workspace_service.py:328 |
| WorkspaceService.unsave_recipe | 保存の解除を本人の履歴へ追記する。 | backend/src/app/core/workspace_service.py:346 |

[SQL](queries.md) / [シーケンス](sequence.md) / [ログ](messages.md) / [要因別テスト](tests.md)
