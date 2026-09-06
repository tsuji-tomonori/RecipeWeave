# 詳細設計: create_cooking_session

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/cooking-sessions` — 調理計画を確定して開始する

## 入力と処理前提

| 項目 | 仕様 |
|---|---|
| authentication | 検証済みBearerトークンと本人所有権 |
| idempotency | 要求のexpectedVersionで再送・同時更新を検出する |
| transaction | 本人のworkspace_revisionをロックし、各正規化行・監査・版を原子的に確定する |
| effects | 正規化された本人の業務データを更新する |

| 入力場所 | 名前 | 型 | 必須 |
|---|---|---|---|

### 本文: application/json

| 入力 | 型 | 必須 | 制約 | 意味 |
|---|---|---|---|---|
| deduct | boolean | 任意 | default=false | Deduct |
| expectedVersion | integer | 必須 | minimum=0.0; maximum=9007199254740990.0 | Expectedversion |
| session | CookingSession | 必須 | 追加制約なし |  |

## データベースの対象と値の流れ

### `backend/src/app/apis/workspace/create_cooking_session/sql/q001_current.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.cooking_session | R | id: 不変の行識別子; created_at: 作成日時（UTC）; menu_id: 対象献立; status: 実行状態; current_task_index: 調理画面の現在の工程位置（0始まり） |
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者 |

対象条件: `WHERE m.user_id = %(user_id)s AND s.status IN ('planned', 'cooking', 'paused')`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

代入・選択式: `s.id; s.menu_id; s.status; s.current_task_index`

### `backend/src/app/apis/workspace/create_cooking_session/sql/q010_recipe.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.recipe | R | id: 不変の行識別子; status: 公開状態 |
| recipeweave.recipe_version | R | id: 不変の行識別子; recipe_id: 所属レシピ; version: 版番号; base_servings: 登録分量が何人前か; status: 版の状態; validation: 公開審査 |

対象条件: `WHERE r.id = %(recipe_id)s AND (CAST(%(requested_version_id)s AS UUID) IS NULL OR rv.id = %(requested_version_id)s) AND ((rv.status = 'published' AND rv.validation = 'passed' AND r.status = 'published') OR (%(preview)s AND rv.status = 'draft' AND r.status = 'draft'))`

| SQLバインド | 実装上の値の出所 |
|---|---|
| preview | 型付きクエリの引数。呼出元のSQL仕様を参照。 |
| recipe_id | 型付きクエリの引数。呼出元のSQL仕様を参照。 |
| requested_version_id | 型付きクエリの引数。呼出元のSQL仕様を参照。 |

代入・選択式: `rv.id; rv.base_servings`

### `backend/src/app/apis/workspace/create_cooking_session/sql/q011_ingredients.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food_form | R | id: 不変の行識別子; food_id: 対応食材 |
| recipeweave.recipe_ingredient | R | id: 不変の行識別子; recipe_version_id: 親版; line_no: 表示順; form_id: 使用形態; amount: 確定値または範囲下限; unit_id: 登録単位; optional: 任意追加材料 |
| recipeweave.unit | R | id: 不変の行識別子; code: 単位コード |

対象条件: `WHERE ri.recipe_version_id = %(version_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| version_id | 型付きクエリの引数。呼出元のSQL仕様を参照。 |

代入・選択式: `ri.id; fm.food_id; ri.amount; ri.optional; ri.unit_id; ri.form_id; u.code AS unit`

### `backend/src/app/apis/workspace/create_cooking_session/sql/q012_menu.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu | C | id: 不変の行識別子; user_id: 所有者; name: 献立名; servings: 標準人数; revision: 楽観ロック版 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| menu_id | menu_id (backend/src/app/core/cooking_service.py:123) / menu_id (backend/src/app/core/cooking_service.py:124) / menu_id (backend/src/app/core/cooking_service.py:125) / menu_id (backend/src/app/core/cooking_service.py:131) / menu_id (backend/src/app/core/cooking_service.py:175) / menu_id (backend/src/app/core/cooking_service.py:141) |
| name | 型付きクエリの引数。呼出元のSQL仕様を参照。 |
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(menu_id)s |
| user_id | %(user_id)s |
| name | %(name)s |
| servings | 2 |
| revision | 1 |

競合時の処理: `ON CONFLICT(id) DO NOTHING`

### `backend/src/app/apis/workspace/create_cooking_session/sql/q013_insert_item.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu_item | CR | id: 不変の行識別子; menu_id: 献立; recipe_version_id: 固定レシピ版; servings: その料理を作る人数; role_option_id: 主菜等; position: 表示順 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| menu_id | menu_id (backend/src/app/core/cooking_service.py:123) / menu_id (backend/src/app/core/cooking_service.py:124) / menu_id (backend/src/app/core/cooking_service.py:125) / menu_id (backend/src/app/core/cooking_service.py:131) / menu_id (backend/src/app/core/cooking_service.py:175) / menu_id (backend/src/app/core/cooking_service.py:141) |
| row_id | task_id (backend/src/app/core/cooking_service.py:187) / uuid4() (backend/src/app/core/cooking_service.py:207) / uuid4() (backend/src/app/core/cooking_service.py:221) / uuid4() (backend/src/app/core/cooking_service.py:197) |
| servings | row['servings'] (backend/src/app/core/cooking_service.py:147) |
| version_id | 型付きクエリの引数。呼出元のSQL仕様を参照。 |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(row_id)s |
| menu_id | %(menu_id)s |
| recipe_version_id | %(version_id)s |
| servings | %(servings)s |
| role_option_id | NULL |
| position | (SELECT COALESCE(MAX(mi.position), 0) + 1 FROM recipeweave.menu_item AS mi WHERE mi.menu_id = %(menu_id)s) |

### `backend/src/app/apis/workspace/create_cooking_session/sql/q014_override.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu_ingredient_override | C | id: 不変の行識別子; menu_item_id: 対象料理; ingredient_line_id: 元材料行; selected: 任意材料を使うか; amount: 適量等の確定基準量; form_id: 明示的代替形態; product_version_id: 購入商品指定 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| amount | amount (backend/src/app/core/cooking_service.py:221) / r['amount'] (backend/src/app/core/cooking_service.py:158) |
| ingredient_id | 型付きクエリの引数。呼出元のSQL仕様を参照。 |
| item_id | task.item_id (backend/src/app/core/cooking_service.py:187) |
| row_id | task_id (backend/src/app/core/cooking_service.py:187) / uuid4() (backend/src/app/core/cooking_service.py:207) / uuid4() (backend/src/app/core/cooking_service.py:221) / uuid4() (backend/src/app/core/cooking_service.py:197) |
| selected | 型付きクエリの引数。呼出元のSQL仕様を参照。 |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(row_id)s |
| menu_item_id | %(item_id)s |
| ingredient_line_id | %(ingredient_id)s |
| selected | %(selected)s |
| amount | %(amount)s |
| form_id | NULL |
| product_version_id | NULL |

### `backend/src/app/apis/workspace/create_cooking_session/sql/q015_advance_menu.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu | U | id: 不変の行識別子; user_id: 所有者; revision: 楽観ロック版 |

対象条件: `WHERE id = %(menu_id)s AND user_id = %(user_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| menu_id | menu_id (backend/src/app/core/cooking_service.py:123) / menu_id (backend/src/app/core/cooking_service.py:124) / menu_id (backend/src/app/core/cooking_service.py:125) / menu_id (backend/src/app/core/cooking_service.py:131) / menu_id (backend/src/app/core/cooking_service.py:175) / menu_id (backend/src/app/core/cooking_service.py:141) |
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| revision | revision + 1 |

代入・選択式: `revision = revision + 1`

### `backend/src/app/apis/workspace/create_cooking_session/sql/q020_steps.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu_item | R | id: 不変の行識別子; menu_id: 献立; recipe_version_id: 固定レシピ版; servings: その料理を作る人数; position: 表示順 |
| recipeweave.recipe_step | R | id: 不変の行識別子; recipe_version_id: 所属版; step_no: 表示順（依存順とは別）; attention: 作業者拘束; duration_max_s: 所要秒上限; scaling_rule_id: 時間の人数変更規則 |
| recipeweave.recipe_version | R | id: 不変の行識別子; recipe_id: 所属レシピ; base_servings: 登録分量が何人前か |
| recipeweave.scaling_rule | R | id: 不変の行識別子; mode: 比例・バッチ等; min_servings: 検証済み人数下限; max_servings: 検証済み人数上限; batch_capacity: 1バッチ上限 |

対象条件: `WHERE mi.menu_id = %(menu_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| menu_id | menu_id (backend/src/app/core/cooking_service.py:123) / menu_id (backend/src/app/core/cooking_service.py:124) / menu_id (backend/src/app/core/cooking_service.py:125) / menu_id (backend/src/app/core/cooking_service.py:131) / menu_id (backend/src/app/core/cooking_service.py:175) / menu_id (backend/src/app/core/cooking_service.py:141) |

代入・選択式: `mi.id AS item_id; mi.position; mi.servings; rv.base_servings; rv.recipe_id; st.id AS step_id; st.step_no; st.duration_max_s; st.attention; sc.mode AS scaling_mode; sc.batch_capacity; sc.min_servings; sc.max_servings`

### `backend/src/app/apis/workspace/create_cooking_session/sql/q021_dependencies.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu_item | R | id: 不変の行識別子; menu_id: 献立; recipe_version_id: 固定レシピ版; position: 表示順 |
| recipeweave.recipe_step | R | id: 不変の行識別子; recipe_version_id: 所属版 |
| recipeweave.step_dependency | R | id: 不変の行識別子; before_step_id: 先行工程; after_step_id: 後続工程; kind: 依存理由; min_lag_s: 完了後最低待機; max_lag_s: 品質上の最大待機 |

対象条件: `WHERE mi.menu_id = %(menu_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| menu_id | menu_id (backend/src/app/core/cooking_service.py:123) / menu_id (backend/src/app/core/cooking_service.py:124) / menu_id (backend/src/app/core/cooking_service.py:125) / menu_id (backend/src/app/core/cooking_service.py:131) / menu_id (backend/src/app/core/cooking_service.py:175) / menu_id (backend/src/app/core/cooking_service.py:141) |

代入・選択式: `mi.id AS item_id; d.before_step_id; d.after_step_id; d.min_lag_s; d.max_lag_s; d.kind`

### `backend/src/app/apis/workspace/create_cooking_session/sql/q022_requirements.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu_item | R | menu_id: 献立; recipe_version_id: 固定レシピ版 |
| recipeweave.recipe_step | R | id: 不変の行識別子; recipe_version_id: 所属版 |
| recipeweave.resource_type | R | id: 不変の行識別子; code: burner/pan/person等; name: 道具名 |
| recipeweave.step_resource | R | step_id: 対象工程; resource_type_id: 要求種別; quantity: 必要台数・人数; capacity_min: 必要最低容量; exclusive: 占有するか |

対象条件: `WHERE EXISTS(SELECT 1 FROM recipeweave.recipe_step AS st INNER JOIN recipeweave.menu_item AS mi ON st.recipe_version_id = mi.recipe_version_id WHERE mi.menu_id = %(menu_id)s AND st.id = sr.step_id)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| menu_id | menu_id (backend/src/app/core/cooking_service.py:123) / menu_id (backend/src/app/core/cooking_service.py:124) / menu_id (backend/src/app/core/cooking_service.py:125) / menu_id (backend/src/app/core/cooking_service.py:131) / menu_id (backend/src/app/core/cooking_service.py:175) / menu_id (backend/src/app/core/cooking_service.py:141) |

代入・選択式: `sr.step_id; sr.resource_type_id; sr.quantity; sr.capacity_min; sr.exclusive; rt.name; rt.code`

### `backend/src/app/apis/workspace/create_cooking_session/sql/q023_resources.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.kitchen_resource | R | id: 不変の行識別子; user_id: 所有者; resource_type_id: コンロ・鍋・人等; name: 左コンロ・26cmフライパン等; capacity: 容量; quantity: 同等資源数; active: 新規の調理計画で利用する資源か |
| recipeweave.resource_type | R | id: 不変の行識別子; code: burner/pan/person等 |

対象条件: `WHERE k.user_id = %(user_id)s AND k.active`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

代入・選択式: `k.id; k.resource_type_id; k.name; k.quantity; k.capacity; rt.code`

### `backend/src/app/apis/workspace/create_cooking_session/sql/q024_ingredients.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu_ingredient_override | R | menu_item_id: 対象料理; ingredient_line_id: 元材料行; selected: 任意材料を使うか; amount: 適量等の確定基準量 |
| recipeweave.menu_item | R | id: 不変の行識別子; menu_id: 献立; recipe_version_id: 固定レシピ版; servings: その料理を作る人数; position: 表示順 |
| recipeweave.recipe_ingredient | R | id: 不変の行識別子; recipe_version_id: 親版; line_no: 表示順; form_id: 使用形態; product_version_id: 商品指定時の仕様版; demand_kind: 購入対象区分; amount: 確定値または範囲下限; unit_id: 登録単位; conversion_id: 非基準単位の換算根拠; optional: 任意追加材料 |
| recipeweave.recipe_version | R | id: 不変の行識別子; base_servings: 登録分量が何人前か |

対象条件: `WHERE mi.menu_id = %(menu_id)s AND ri.demand_kind <> 'kit_component' AND (NOT ri.optional OR ov.selected)`

| SQLバインド | 実装上の値の出所 |
|---|---|
| menu_id | menu_id (backend/src/app/core/cooking_service.py:123) / menu_id (backend/src/app/core/cooking_service.py:124) / menu_id (backend/src/app/core/cooking_service.py:125) / menu_id (backend/src/app/core/cooking_service.py:131) / menu_id (backend/src/app/core/cooking_service.py:175) / menu_id (backend/src/app/core/cooking_service.py:141) |

代入・選択式: `ri.id AS ingredient_id; ri.form_id; ri.product_version_id; ri.unit_id; ri.conversion_id; mi.id AS item_id; rv.id AS recipe_version_id; mi.servings; COALESCE(ov.amount, ri.amount * mi.servings / rv.base_servings) AS amount`

### `backend/src/app/apis/workspace/create_cooking_session/sql/q025_session.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.cooking_session | C | id: 不変の行識別子; menu_id: 対象献立; menu_revision: 献立版; status: 実行状態; target_at: 完成希望時刻; planner_version: 計画器の版; input_snapshot: 材料・資源・人数の固定入力; input_hash: 入力ハッシュ |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| hash | hashlib.sha256(encoded.encode()).hexdigest() (backend/src/app/core/cooking_service.py:175) |
| menu_id | menu_id (backend/src/app/core/cooking_service.py:123) / menu_id (backend/src/app/core/cooking_service.py:124) / menu_id (backend/src/app/core/cooking_service.py:125) / menu_id (backend/src/app/core/cooking_service.py:131) / menu_id (backend/src/app/core/cooking_service.py:175) / menu_id (backend/src/app/core/cooking_service.py:141) |
| revision | revision (backend/src/app/core/cooking_service.py:175) |
| session_id | session_id (backend/src/app/core/cooking_service.py:175) / session_id (backend/src/app/core/cooking_service.py:187) / session_id (backend/src/app/core/cooking_service.py:221) |
| snapshot | Jsonb(snapshot.model_dump(mode='json')) (backend/src/app/core/cooking_service.py:175) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(session_id)s |
| menu_id | %(menu_id)s |
| menu_revision | %(revision)s |
| status | 'cooking' |
| target_at | NULL |
| planner_version | 'dag-resource-v1' |
| input_snapshot | %(snapshot)s |
| input_hash | %(hash)s |

### `backend/src/app/apis/workspace/create_cooking_session/sql/q026_task.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.session_task | C | id: 不変の行識別子; session_id: 実行; menu_item_id: 料理; step_id: 元工程; batch_no: 容量分割した回; planned_start_s: 開始相対秒; planned_end_s: 終了相対秒; status: 進捗 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| end | task.end (backend/src/app/core/cooking_service.py:187) / task.end (backend/src/app/core/cooking_service.py:197) |
| item_id | task.item_id (backend/src/app/core/cooking_service.py:187) |
| row_id | task_id (backend/src/app/core/cooking_service.py:187) / uuid4() (backend/src/app/core/cooking_service.py:207) / uuid4() (backend/src/app/core/cooking_service.py:221) / uuid4() (backend/src/app/core/cooking_service.py:197) |
| session_id | session_id (backend/src/app/core/cooking_service.py:175) / session_id (backend/src/app/core/cooking_service.py:187) / session_id (backend/src/app/core/cooking_service.py:221) |
| start | task.start (backend/src/app/core/cooking_service.py:187) / task.start (backend/src/app/core/cooking_service.py:197) |
| step_id | task.step_id (backend/src/app/core/cooking_service.py:187) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(row_id)s |
| session_id | %(session_id)s |
| menu_item_id | %(item_id)s |
| step_id | %(step_id)s |
| batch_no | 1 |
| planned_start_s | %(start)s |
| planned_end_s | %(end)s |
| status | 'pending' |

### `backend/src/app/apis/workspace/create_cooking_session/sql/q027_dependency.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.task_dependency | C | id: 不変の行識別子; before_task_id: 先行タスク; after_task_id: 後続タスク; min_lag_s: 最小間隔; max_lag_s: 最大間隔; reason: 元DAG/洗浄/設備切替等 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| after_id | task_ids[dependency['item_id'], dependency['after_step_id']] (backend/src/app/core/cooking_service.py:207) |
| before_id | task_ids[dependency['item_id'], dependency['before_step_id']] (backend/src/app/core/cooking_service.py:207) |
| max_lag | dependency['max_lag_s'] (backend/src/app/core/cooking_service.py:207) |
| min_lag | dependency['min_lag_s'] (backend/src/app/core/cooking_service.py:207) |
| reason | dependency['kind'] (backend/src/app/core/cooking_service.py:207) |
| row_id | task_id (backend/src/app/core/cooking_service.py:187) / uuid4() (backend/src/app/core/cooking_service.py:207) / uuid4() (backend/src/app/core/cooking_service.py:221) / uuid4() (backend/src/app/core/cooking_service.py:197) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(row_id)s |
| before_task_id | %(before_id)s |
| after_task_id | %(after_id)s |
| min_lag_s | %(min_lag)s |
| max_lag_s | %(max_lag)s |
| reason | %(reason)s |

### `backend/src/app/apis/workspace/create_cooking_session/sql/q028_reservation.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.resource_reservation | C | id: 不変の行識別子; task_id: 使用タスク; resource_id: 実資源; start_s: 占有開始; end_s: 占有終了; quantity: 占有量 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| end | task.end (backend/src/app/core/cooking_service.py:187) / task.end (backend/src/app/core/cooking_service.py:197) |
| quantity | count (backend/src/app/core/cooking_service.py:197) |
| resource_id | resource_id (backend/src/app/core/cooking_service.py:197) |
| row_id | task_id (backend/src/app/core/cooking_service.py:187) / uuid4() (backend/src/app/core/cooking_service.py:207) / uuid4() (backend/src/app/core/cooking_service.py:221) / uuid4() (backend/src/app/core/cooking_service.py:197) |
| start | task.start (backend/src/app/core/cooking_service.py:187) / task.start (backend/src/app/core/cooking_service.py:197) |
| task_id | task_id (backend/src/app/core/cooking_service.py:197) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(row_id)s |
| task_id | %(task_id)s |
| resource_id | %(resource_id)s |
| start_s | %(start)s |
| end_s | %(end)s |
| quantity | %(quantity)s |

### `backend/src/app/apis/workspace/create_cooking_session/sql/q029_total.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.ingredient_total | C | id: 不変の行識別子; session_id: 固定計算対象; form_id: 合算可能な形態; product_version_id: 商品固定; unit_id: 基準単位; required_amount: 必要量; quality: 最も低い入力精度; calculation_version: 計算器版 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| amount | amount (backend/src/app/core/cooking_service.py:221) / r['amount'] (backend/src/app/core/cooking_service.py:158) |
| form_id | form_id (backend/src/app/core/cooking_service.py:221) / r['form_id'] (backend/src/app/core/cooking_service.py:157) |
| product_id | product_id (backend/src/app/core/cooking_service.py:221) |
| row_id | task_id (backend/src/app/core/cooking_service.py:187) / uuid4() (backend/src/app/core/cooking_service.py:207) / uuid4() (backend/src/app/core/cooking_service.py:221) / uuid4() (backend/src/app/core/cooking_service.py:197) |
| session_id | session_id (backend/src/app/core/cooking_service.py:175) / session_id (backend/src/app/core/cooking_service.py:187) / session_id (backend/src/app/core/cooking_service.py:221) |
| unit_id | unit_id (backend/src/app/core/cooking_service.py:221) / r['unit_id'] (backend/src/app/core/cooking_service.py:159) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| id | %(row_id)s |
| session_id | %(session_id)s |
| form_id | %(form_id)s |
| product_version_id | %(product_id)s |
| unit_id | %(unit_id)s |
| required_amount | %(amount)s |
| quality | 'reference' |
| calculation_version | 'decimal-v1' |

### `backend/src/app/apis/workspace/create_cooking_session/sql/q030_menu_revision.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者; revision: 楽観ロック版 |

対象条件: `WHERE id = %(menu_id)s AND user_id = %(user_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| menu_id | menu_id (backend/src/app/core/cooking_service.py:123) / menu_id (backend/src/app/core/cooking_service.py:124) / menu_id (backend/src/app/core/cooking_service.py:125) / menu_id (backend/src/app/core/cooking_service.py:131) / menu_id (backend/src/app/core/cooking_service.py:175) / menu_id (backend/src/app/core/cooking_service.py:141) |
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

代入・選択式: `revision`

### `backend/src/app/apis/workspace/create_cooking_session/sql/q900_lock_revision.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.workspace_revision | R | user_id: 所有者; revision: 全体のCAS版 |

対象条件: `WHERE user_id = %(user_id)s`

行ロック: `FOR UPDATE`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

代入・選択式: `revision`

### `backend/src/app/apis/workspace/create_cooking_session/sql/q901_advance_revision.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.workspace_revision | U | user_id: 所有者; revision: 全体のCAS版 |

対象条件: `WHERE user_id = %(user_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

変更する列とSQL式

| 書込み列 | 値・式（バインド元は上表） |
|---|---|
| revision | revision + 1 |

代入・選択式: `revision = revision + 1`

### `backend/src/app/apis/workspace/create_cooking_session/sql/q902_append_audit.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.audit_event | C | id: 不変の行識別子; actor_id: 実行者（削除時匿名化）; action: publish/withdraw/erase等; entity_type: 対象テーブルの許可リスト; entity_key_hash: 対象識別子のハッシュ; reason: 理由（個人情報を含めない）; occurred_at: 時刻 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| action | 型付きクエリの引数。呼出元のSQL仕様を参照。 |
| key_hash | 型付きクエリの引数。呼出元のSQL仕様を参照。 |
| row_id | task_id (backend/src/app/core/cooking_service.py:187) / uuid4() (backend/src/app/core/cooking_service.py:207) / uuid4() (backend/src/app/core/cooking_service.py:221) / uuid4() (backend/src/app/core/cooking_service.py:197) |
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

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
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

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
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

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
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

代入・選択式: `c.lot_id; c.amount; u.code AS unit; c.session_id`

### `backend/src/app/apis/workspace/get_workspace/sql/q004_receipts.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.receipt_import | R | id: 不変の行識別子; created_at: 作成日時（UTC）; user_id: 所有者; file_sha256: 画像本文のSHA256。本文はDBに保存しない; idempotency_key: 本人内で一意の再送防止キー; status: draft/committed/revertedの状態; reverted_at: 登録取消日時 |

対象条件: `WHERE r.user_id = %(user_id)s AND r.status IN ('committed', 'reverted')`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

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
| menu_id | menu_id (backend/src/app/core/cooking_service.py:123) / menu_id (backend/src/app/core/cooking_service.py:124) / menu_id (backend/src/app/core/cooking_service.py:125) / menu_id (backend/src/app/core/cooking_service.py:131) / menu_id (backend/src/app/core/cooking_service.py:175) / menu_id (backend/src/app/core/cooking_service.py:141) |
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

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
| menu_id | menu_id (backend/src/app/core/cooking_service.py:123) / menu_id (backend/src/app/core/cooking_service.py:124) / menu_id (backend/src/app/core/cooking_service.py:125) / menu_id (backend/src/app/core/cooking_service.py:131) / menu_id (backend/src/app/core/cooking_service.py:175) / menu_id (backend/src/app/core/cooking_service.py:141) |
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

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
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

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
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

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
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

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
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

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
| user_id | self.user_id (backend/src/app/core/cooking_service.py:113) / self.user_id (backend/src/app/core/cooking_service.py:126) / self.user_id (backend/src/app/core/cooking_service.py:141) |

代入・選択式: `s.id; s.menu_id; s.status; s.current_task_index; s.input_snapshot`

### `backend/src/app/apis/workspace/get_workspace/sql/q012_tasks.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.menu_item | R | id: 不変の行識別子; recipe_version_id: 固定レシピ版; position: 表示順 |
| recipeweave.recipe | R | id: 不変の行識別子; title: 代表名 |
| recipeweave.recipe_step | R | id: 不変の行識別子; step_no: 表示順（依存順とは別）; instruction: 個別補足; attention: 作業者拘束; duration_max_s: 所要秒上限; title: 工程の短い見出し |
| recipeweave.recipe_version | R | id: 不変の行識別子; recipe_id: 所属レシピ |
| recipeweave.session_task | R | id: 不変の行識別子; session_id: 実行; menu_item_id: 料理; step_id: 元工程; planned_start_s: 開始相対秒; planned_end_s: 終了相対秒; status: 進捗; timer_started_at: 稼働中タイマーの開始日時; timer_duration_s: 利用者が設定したタイマー秒数 |

対象条件: `WHERE t.session_id = %(session_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| session_id | session_id (backend/src/app/core/cooking_service.py:175) / session_id (backend/src/app/core/cooking_service.py:187) / session_id (backend/src/app/core/cooking_service.py:221) |

代入・選択式: `t.id; t.menu_item_id; t.step_id; t.planned_start_s; t.planned_end_s; t.status; t.timer_started_at; t.timer_duration_s; rv.recipe_id; r.title AS recipe_name; st.title; st.instruction; st.attention; st.duration_max_s`

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
| session_id | session_id (backend/src/app/core/cooking_service.py:175) / session_id (backend/src/app/core/cooking_service.py:187) / session_id (backend/src/app/core/cooking_service.py:221) |

代入・選択式: `t.id AS task_id; r.name`

### `backend/src/app/apis/workspace/get_workspace/sql/q014_totals.sql`

実行条件: 共有処理 get_workspace を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.food_form | R | id: 不変の行識別子; food_id: 対応食材; name: 生皮付き・冷凍刻み等 |
| recipeweave.ingredient_total | R | id: 不変の行識別子; session_id: 固定計算対象; form_id: 合算可能な形態; product_version_id: 商品固定; unit_id: 基準単位; required_amount: 必要量; actual_amount: 利用者が確定した実使用量。不明はNULL; consumption_outcome: 未要求・反映済み・在庫不足・数量不明・単位不一致の結果 |
| recipeweave.pantry_consumption | R | id: 不変の行識別子; session_id: 消費した調理セッション; lot_id: 消費元ロット; amount: 消費数量 |
| recipeweave.pantry_lot | R | id: 不変の行識別子; form_id: 食材形態; product_version_id: 商品版; unit_id: 単位 |
| recipeweave.unit | R | id: 不変の行識別子; code: 単位コード |

対象条件: `WHERE total.session_id = %(session_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| session_id | session_id (backend/src/app/core/cooking_service.py:175) / session_id (backend/src/app/core/cooking_service.py:187) / session_id (backend/src/app/core/cooking_service.py:221) |

代入・選択式: `total.id; fm.food_id; fm.name AS form; total.required_amount; total.actual_amount; total.consumption_outcome; u.code AS unit; COALESCE(SUM(c.amount), 0) AS consumed_amount; ARRAY_AGG(c.lot_id) FILTER(WHERE c.id IS NOT NULL) AS lot_ids`

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
| q.run('q001_current', user_id=self.user_id) | HTTPException(409, '調理中の料理を再開するか、完了してから始めてください') | backend/src/app/core/cooking_service.py:108 |
| not request.session.meal_snapshot | HTTPException(422, '調理する料理を選んでください') | backend/src/app/core/cooking_service.py:108 |
| any((r['amount'] is None for r in ingredients)) | HTTPException(422, '調理前に材料の量を確定してください') | backend/src/app/core/cooking_service.py:108 |
| any((len(values) &gt; 1 for values in identities.values())) | HTTPException(422, '同じ食材の複数商品は、商品版ごとの調理APIで指定してください') | backend/src/app/core/cooking_service.py:108 |

## 出力

| 関数 | 返却式 | 定義元 |
|---|---|---|
| handle | execute(WorkspaceService(database, identity), request) | backend/src/app/apis/workspace/create_cooking_session/router.py:22 |
| execute | service.create_cooking_session(request) | backend/src/app/apis/workspace/create_cooking_session/functions.py:6 |
| WorkspaceService.create_cooking_session | CookingService(self).create(request) | backend/src/app/core/workspace_service.py:486 |
| CookingService.create | self.workspace.finish(q) | backend/src/app/core/cooking_service.py:108 |

APIとして返す型・status・headerは [インターフェース](interface.md) の実OpenAPIを参照。

## 責務

| 関数 | 処理 | 定義元 |
|---|---|---|
| handle | 調理計画を確定して開始する。呼出元が送った利用者IDは使用しない。 | backend/src/app/apis/workspace/create_cooking_session/router.py:22 |
| execute | 調理計画を確定して開始する。永続値は業務サービスが検証し、同一トランザクションで扱う。 | backend/src/app/apis/workspace/create_cooking_session/functions.py:6 |
| WorkspaceService.create_cooking_session | DBの料理と材料から調理計画を構築する。 | backend/src/app/core/workspace_service.py:486 |
| CookingService.create | 画面から送られた計画を信用せず、DBのDAGと設備で再計画する。 | backend/src/app/core/cooking_service.py:108 |

[SQL](queries.md) / [シーケンス](sequence.md) / [ログ](messages.md) / [要因別テスト](tests.md)
