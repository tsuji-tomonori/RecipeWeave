# 詳細設計: random_recipe

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/recipes/random` — 保存済みの料理から一品を選ぶ

## 入力と処理前提

| 項目 | 仕様 |
|---|---|
| authentication | public; previewには開発環境の認証が必要 |
| idempotency | 読取専用。再要求では別の候補になることがある |
| transaction | 要求単位の読取トランザクション |
| effects | レシピと材料・工程・分類の参照 |

| 入力場所 | 名前 | 型 | 必須 |
|---|---|---|---|
| query | excludeId | anyOf(string (uuid), null) | False |
| query | excludedFoodIds | array&lt;string (uuid)&gt; | False |
| query | preview | boolean | False |

## データベースの対象と値の流れ

### `backend/src/app/apis/recipes/random_recipe/sql/001_random_recipe.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.axis_option | R | id: 不変の行識別子; label: 候補名 |
| recipeweave.compatibility_rule | R | id: 不変の行識別子; code: 規則コード |
| recipeweave.food_form | R | id: 不変の行識別子; food_id: 対応食材; name: 生皮付き・冷凍刻み等 |
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
| recipeweave.validation_result | R | recipe_version_id: 対象版; rule_id: 適用規則版; state: 結果 |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| equipment | equipment or [] (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| exclude_id | search.exclude_id (backend/src/app/apis/recipes/random_recipe/functions.py:8) / exclude_id (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| excluded_food_ids | search.excluded_food_ids (backend/src/app/apis/recipes/random_recipe/functions.py:8) / excluded_food_ids or [] (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| limit | 1 (backend/src/app/apis/recipes/random_recipe/functions.py:8) / limit (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| match | match (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| max_minutes | max_minutes (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| offset | offset (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| preview | search.preview (backend/src/app/apis/recipes/random_recipe/functions.py:8) / preview (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| q | query (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| recipe_id | recipe_id (backend/src/app/integrations/catalog/postgres_provider.py:48) |
| selected_food_ids | selected_food_ids or [] (backend/src/app/integrations/catalog/postgres_provider.py:48) |

代入・選択式: `COALESCE(JSONB_AGG(payloads.payload ORDER BY payloads.title, payloads.id), CAST('[]' AS JSONB)) AS items; (SELECT COUNT(matched.id) FROM matched) AS total`

### `backend/src/app/apis/auth/get_me/sql/q001_set_identity.sql`

実行条件: 試用を許可した開発環境でpreview=trueとして認証する場合のみ。通常の公開検索では実行しない。

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| role | identity.role (backend/src/app/core/identity.py:82) |
| user_id | str(identity.user_id) (backend/src/app/core/identity.py:82) / identity.user_id (backend/src/app/core/identity.py:83) / identity.user_id (backend/src/app/core/identity.py:86) / identity.user_id (backend/src/app/core/identity.py:89) / identity.user_id (backend/src/app/core/identity.py:96) |

代入・選択式: `SET_CONFIG('recipeweave.user_id', %(user_id)s, TRUE) AS user_setting; SET_CONFIG('recipeweave.role', %(role)s, TRUE) AS role_setting`

### `backend/src/app/apis/auth/get_me/sql/q002_initialize_user.sql`

実行条件: 試用を許可した開発環境でpreview=trueとして認証する場合のみ。通常の公開検索では実行しない。

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

実行条件: 試用を許可した開発環境でpreview=trueとして認証する場合のみ。通常の公開検索では実行しない。

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

実行条件: 試用を許可した開発環境でpreview=trueとして認証する場合のみ。通常の公開検索では実行しない。

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

実行条件: 試用を許可した開発環境でpreview=trueとして認証する場合のみ。通常の公開検索では実行しない。

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

## 出力

| 関数 | 返却式 | 定義元 |
|---|---|---|
| random_recipe | api_functions.random_recipe(catalog, search) | backend/src/app/apis/recipes/random_recipe/router.py:29 |
| random_recipe | RandomRecipeResponse(item=items[0] if items else None, total=total) | backend/src/app/apis/recipes/random_recipe/functions.py:6 |
| PostgresCatalog.recipes | ([Recipe.model_validate(row) for row in rows[0]['items']], int(rows[0]['total'])) | backend/src/app/integrations/catalog/postgres_provider.py:24 |

APIとして返す型・status・headerは [インターフェース](interface.md) の実OpenAPIを参照。

## 責務

| 関数 | 処理 | 定義元 |
|---|---|---|
| random_recipe | 個別説明なし | backend/src/app/apis/recipes/random_recipe/router.py:29 |
| random_recipe | 除外食材と前回の一品を除いて選ぶ。候補ゼロならnullを返す。 | backend/src/app/apis/recipes/random_recipe/functions.py:6 |
| PostgresCatalog.recipes | 個別説明なし | backend/src/app/integrations/catalog/postgres_provider.py:24 |

[SQL](queries.md) / [シーケンス](sequence.md) / [ログ](messages.md) / [要因別テスト](tests.md)
