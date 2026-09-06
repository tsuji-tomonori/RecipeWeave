# 詳細設計: preview_cooking_plan

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/cooking-plan` — 保存せずに調理の段取りを確認する

## 入力と処理前提

| 項目 | 仕様 |
|---|---|
| authentication | 検証済みBearerトークンと本人所有権 |
| idempotency | 読取専用。同じDB状態と入力は同じ計画を返す |
| transaction | 要求単位の読取。献立・調理・監査・版の更新を行わない |
| effects | 閲覧可能な指定料理版の材料と工程、依存関係、本人の設備を読み、開始時と共通の計画器で検証する |

| 入力場所 | 名前 | 型 | 必須 |
|---|---|---|---|

### 本文: application/json

| 入力 | 型 | 必須 | 制約 | 意味 |
|---|---|---|---|---|
| durationEstimates | array&lt;DurationEstimate&gt; | 任意 | maxItems=500 | Durationestimates |
| items | array&lt;MealItem&gt; | 必須 | minItems=1; maxItems=50 | Items |

## データベースの対象と値の流れ

### `backend/src/app/apis/workspace/preview_cooking_plan/sql/q001_steps.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.recipe_ingredient | R | recipe_version_id: 親版; scaling_rule_id: 人数変換規則 |
| recipeweave.recipe_step | R | id: 不変の行識別子; recipe_version_id: 所属版; step_no: 表示順（依存順とは別）; attention: 作業者拘束; duration_max_s: 所要秒上限; scaling_rule_id: 時間の人数変更規則 |
| recipeweave.recipe_version | R | id: 不変の行識別子; recipe_id: 所属レシピ; base_servings: 登録分量が何人前か |
| recipeweave.scaling_rule | R | id: 不変の行識別子; mode: 比例・バッチ等; min_servings: 検証済み人数下限; max_servings: 検証済み人数上限; batch_capacity: 1バッチ上限 |

対象条件: `WHERE rv.id = %(version_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| item_id | item_id (backend/src/app/core/cooking_plan_service.py:86) / item_id (backend/src/app/core/cooking_plan_service.py:95) |
| position | position (backend/src/app/core/cooking_plan_service.py:86) |
| servings | item.servings (backend/src/app/core/cooking_plan_service.py:86) |
| version_id | _uuid(item.recipe_version_id) (backend/src/app/core/cooking_plan_service.py:72) / version_id (backend/src/app/core/cooking_plan_service.py:97) / version_id (backend/src/app/core/cooking_plan_service.py:86) / version_id (backend/src/app/core/cooking_plan_service.py:95) / version_id (backend/src/app/integrations/catalog/postgres_provider.py:62) |

代入・選択式: `CAST(%(item_id)s AS UUID) AS item_id; CAST(%(position)s AS INT) AS position; CAST(%(servings)s AS DECIMAL) AS servings; rv.base_servings; rv.recipe_id; st.id AS step_id; st.step_no; st.duration_max_s; st.attention; sc.mode AS scaling_mode; sc.batch_capacity; GREATEST(sc.min_servings, (SELECT MAX(ingredient_rule.min_servings) FROM recipeweave.recipe_ingredient AS ingredient INNER JOIN recipeweave.scaling_rule AS ingredient_rule ON ingredient.scaling_rule_id = ingredient_rule.id WHERE ingredient.recipe_version_id = rv.id)) AS min_servings; LEAST(sc.max_servings, (SELECT MIN(ingredient_rule.max_servings) FROM recipeweave.recipe_ingredient AS ingredient INNER JOIN recipeweave.scaling_rule AS ingredient_rule ON ingredient.scaling_rule_id = ingredient_rule.id WHERE ingredient.recipe_version_id = rv.id)) AS max_servings`

### `backend/src/app/apis/workspace/preview_cooking_plan/sql/q002_dependencies.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.recipe_step | R | id: 不変の行識別子; recipe_version_id: 所属版 |
| recipeweave.step_dependency | R | id: 不変の行識別子; before_step_id: 先行工程; after_step_id: 後続工程; kind: 依存理由; min_lag_s: 完了後最低待機; max_lag_s: 品質上の最大待機 |

対象条件: `WHERE st.recipe_version_id = %(version_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| item_id | item_id (backend/src/app/core/cooking_plan_service.py:86) / item_id (backend/src/app/core/cooking_plan_service.py:95) |
| version_id | _uuid(item.recipe_version_id) (backend/src/app/core/cooking_plan_service.py:72) / version_id (backend/src/app/core/cooking_plan_service.py:97) / version_id (backend/src/app/core/cooking_plan_service.py:86) / version_id (backend/src/app/core/cooking_plan_service.py:95) / version_id (backend/src/app/integrations/catalog/postgres_provider.py:62) |

代入・選択式: `CAST(%(item_id)s AS UUID) AS item_id; d.before_step_id; d.after_step_id; d.min_lag_s; d.max_lag_s; d.kind`

### `backend/src/app/apis/workspace/preview_cooking_plan/sql/q003_requirements.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.recipe_step | R | id: 不変の行識別子; recipe_version_id: 所属版 |
| recipeweave.resource_type | R | id: 不変の行識別子; code: burner/pan/person等; name: 道具名 |
| recipeweave.step_resource | R | step_id: 対象工程; resource_type_id: 要求種別; quantity: 必要台数・人数; capacity_min: 必要最低容量; exclusive: 占有するか |

対象条件: `WHERE st.recipe_version_id = %(version_id)s`

| SQLバインド | 実装上の値の出所 |
|---|---|
| version_id | _uuid(item.recipe_version_id) (backend/src/app/core/cooking_plan_service.py:72) / version_id (backend/src/app/core/cooking_plan_service.py:97) / version_id (backend/src/app/core/cooking_plan_service.py:86) / version_id (backend/src/app/core/cooking_plan_service.py:95) / version_id (backend/src/app/integrations/catalog/postgres_provider.py:62) |

代入・選択式: `sr.step_id; sr.resource_type_id; sr.quantity; sr.capacity_min; sr.exclusive; rt.name; rt.code`

### `backend/src/app/apis/workspace/preview_cooking_plan/sql/q004_resources.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.kitchen_resource | R | id: 不変の行識別子; user_id: 所有者; resource_type_id: コンロ・鍋・人等; name: 左コンロ・26cmフライパン等; capacity: 容量; quantity: 同等資源数; active: 新規の調理計画で利用する資源か |
| recipeweave.resource_type | R | id: 不変の行識別子; code: burner/pan/person等 |

対象条件: `WHERE k.user_id = %(user_id)s AND k.active`

| SQLバインド | 実装上の値の出所 |
|---|---|
| user_id | self.identity.user_id (backend/src/app/core/cooking_plan_service.py:99) |

代入・選択式: `k.id; k.resource_type_id; k.name; k.quantity; k.capacity; rt.code`

### `backend/src/app/apis/recipes/get_recipe/sql/001_select_recipe.sql`

実行条件: 共有処理 get_recipe を呼ぶ経路。分岐・反復は詳細設計の実関数を参照。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.axis_option | R | id: 不変の行識別子; label: 候補名 |
| recipeweave.compatibility_rule | R | id: 不変の行識別子; code: 規則コード |
| recipeweave.food_form | R | id: 不変の行識別子; food_id: 対応食材; name: 生皮付き・冷凍刻み等 |
| recipeweave.menu | R | id: 不変の行識別子; user_id: 所有者 |
| recipeweave.menu_item | R | menu_id: 献立; recipe_version_id: 固定レシピ版 |
| recipeweave.operation | R | id: 不変の行識別子; code: cut_ginkgo等; name: いちょう切り等 |
| recipeweave.recipe | R | id: 不変の行識別子; title: 代表名; status: 公開状態; withdrawal_reason: 取下げ理由 |
| recipeweave.recipe_ingredient | R | id: 不変の行識別子; recipe_version_id: 親版; line_no: 表示順; form_id: 使用形態; product_version_id: 商品指定時の仕様版; amount: 確定値または範囲下限; unit_id: 登録単位; note: 材料の補足 |
| recipeweave.recipe_option | R | recipe_version_id: 対象版; option_id: 特徴値 |
| recipeweave.recipe_step | R | id: 不変の行識別子; recipe_version_id: 所属版; step_no: 表示順（依存順とは別）; operation_id: 標準動作; instruction: 個別補足; attention: 作業者拘束; duration_max_s: 所要秒上限; scaling_rule_id: 時間の人数変更規則; title: 工程の短い見出し |
| recipeweave.recipe_version | R | id: 不変の行識別子; recipe_id: 所属レシピ; version: 版番号; base_servings: 登録分量が何人前か; status: 版の状態; validation: 公開審査; description: 料理の紹介文 |
| recipeweave.resource_type | R | id: 不変の行識別子; code: burner/pan/person等; name: 道具名 |
| recipeweave.scaling_rule | R | id: 不変の行識別子; mode: 比例・バッチ等 |
| recipeweave.step_resource | R | step_id: 対象工程; resource_type_id: 要求種別 |
| recipeweave.unit | R | id: 不変の行識別子; code: 単位コード |
| recipeweave.user_recipe_event | R | user_id: 利用者; recipe_version_id: 提案版 |
| recipeweave.validation_result | R | recipe_version_id: 対象版; rule_id: 適用規則版; state: 結果 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| equipment | [resource_names[resource_id] for resource_id, _ in task.reservations] (backend/src/app/core/cooking_plan_service.py:130) / equipment or [] (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| exclude_id | exclude_id (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| excluded_food_ids | excluded_food_ids or [] (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| limit | limit (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| match | match (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| max_minutes | max_minutes (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| offset | offset (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| owner_id | self.identity.user_id (backend/src/app/core/cooking_plan_service.py:72) / owner_id (backend/src/app/integrations/catalog/postgres_provider.py:62) |
| preview | catalog_preview_enabled() (backend/src/app/core/cooking_plan_service.py:72) / preview (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| q | query (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| recipe_id | _uuid(item.recipe_id) (backend/src/app/core/cooking_plan_service.py:72) / recipe.id (backend/src/app/core/cooking_plan_service.py:123) / recipe_id (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| selected_food_ids | selected_food_ids or [] (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| version_id | _uuid(item.recipe_version_id) (backend/src/app/core/cooking_plan_service.py:72) / version_id (backend/src/app/core/cooking_plan_service.py:97) / version_id (backend/src/app/core/cooking_plan_service.py:86) / version_id (backend/src/app/core/cooking_plan_service.py:95) / version_id (backend/src/app/integrations/catalog/postgres_provider.py:62) |

代入・選択式: `COALESCE(JSONB_AGG(payloads.payload ORDER BY payloads.title, payloads.id), CAST('[]' AS JSONB)) AS items; (SELECT COUNT(matched.id) FROM matched) AS total`

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
| None in keys or set(item.amounts) != keys | HTTPException(422, '指定した料理版と材料の構成が一致しません') | backend/src/app/core/cooking_plan_service.py:40 |
| ingredient.ingredient_id is None | HTTPException(422, '材料行の識別子が登録されていません') | backend/src/app/core/cooking_plan_service.py:40 |
| amount.value is None or amount.unit != ingredient.quantity.unit | HTTPException(422, '材料の量を確定し、登録済みの単位で指定してください') | backend/src/app/core/cooking_plan_service.py:40 |
| item_id in recipes | HTTPException(422, '同じ献立行が重複しています') | backend/src/app/core/cooking_plan_service.py:60 |
| not recipe_rows | HTTPException(404, 'この料理版は利用できません') | backend/src/app/core/cooking_plan_service.py:60 |

## 出力

| 関数 | 返却式 | 定義元 |
|---|---|---|
| handle | execute(CookingPlanService(database, identity), request) | backend/src/app/apis/workspace/preview_cooking_plan/router.py:22 |
| execute | service.preview(request) | backend/src/app/apis/workspace/preview_cooking_plan/functions.py:4 |
| _uuid | UUID(value or '') | backend/src/app/core/cooking_plan_service.py:33 |
| CookingPlanService.preview | PlanResponse(plan=result) | backend/src/app/core/cooking_plan_service.py:60 |
| PostgresCatalog.recipes | ([Recipe.model_validate(row) for row in rows[0]['items']], int(rows[0]['total'])) | backend/src/app/integrations/catalog/postgres_provider.py:24 |

APIとして返す型・status・headerは [インターフェース](interface.md) の実OpenAPIを参照。

## 責務

| 関数 | 処理 | 定義元 |
|---|---|---|
| handle | 実際の調理開始と同じ規則で、表示する段取りを計算する。 | backend/src/app/apis/workspace/preview_cooking_plan/router.py:22 |
| execute | 献立の版と分量を検証して、永続化せず段取りを返す。 | backend/src/app/apis/workspace/preview_cooking_plan/functions.py:4 |
| _uuid | 個別説明なし | backend/src/app/core/cooking_plan_service.py:33 |
| validate_item | 同一食品の複数材料行を混同せず、単位や未知量の不整合を拒否する。 | backend/src/app/core/cooking_plan_service.py:40 |
| CookingPlanService.preview | 最新の設備と閲覧可能な料理版から、変更を保存せず計算する。 | backend/src/app/core/cooking_plan_service.py:60 |
| PostgresCatalog.recipes | 個別説明なし | backend/src/app/integrations/catalog/postgres_provider.py:24 |

[SQL](queries.md) / [シーケンス](sequence.md) / [ログ](messages.md) / [要因別テスト](tests.md)
