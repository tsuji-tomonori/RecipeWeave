# 詳細設計: list_foods

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/foods` — 食材候補を検索する

## 入力と処理前提

| 項目 | 仕様 |
|---|---|
| authentication | public |
| idempotency | 読取専用 |
| transaction | 要求単位の読取トランザクション |
| effects | 食品・形態・分類・別名の参照 |

| 入力場所 | 名前 | 型 | 必須 |
|---|---|---|---|
| query | q | string | False |

## データベースの対象と値の流れ

### `backend/src/app/apis/foods/list_foods/sql/001_select_foods.sql`

実行条件: このSQLの呼出し経路で実行

| 物理テーブル | 操作 | 対象列と意味 |
|---|---|---|
| recipeweave.axis | R | id: 不変の行識別子; code: 軸コード |
| recipeweave.axis_option | R | id: 不変の行識別子; axis_id: 親軸; code: 値コード; label: 候補名 |
| recipeweave.food | R | id: 不変の行識別子; name: 食材名・加工品種別; kind: 基本食材か加工食品か; status: 新規使用可否 |
| recipeweave.food_alias | R | food_id: 正規食材; alias: 別名・かな; locale: 言語・地域 |
| recipeweave.food_axis_option | R | food_id: 食材; option_id: カテゴリ・入手性等の値 |
| recipeweave.food_form | R | id: 不変の行識別子; food_id: 対応食材; name: 生皮付き・冷凍刻み等; state: 処理状態; base_unit_id: 計算基準単位; status: 利用状態 |
| recipeweave.unit | R | id: 不変の行識別子; code: 単位コード |

対象条件: `SQL上の絞り込みなし`

| SQLバインド | 実装上の値の出所 |
|---|---|
| q | query (backend/src/app/integrations/catalog/postgres_provider.py:19) |

代入・選択式: `COALESCE(JSONB_AGG(JSONB_BUILD_OBJECT('id', CAST(available.id AS TEXT), 'name', available.name, 'aliases', available.aliases, 'category', available.category, 'defaultUnit', available.unit_code, 'location', available.storage_location, 'pantry', available.pantry, 'imageIndex', NULL, 'componentsKnown', available.kind IN ('basic', 'utility'), 'componentFoodIds', CAST('[]' AS JSONB)) ORDER BY available.name, available.id), CAST('[]' AS JSONB)) AS items; COUNT(available.id) AS total`

## 分岐・拒否条件

| 判定条件 | 例外・応答 | 定義元 |
|---|---|---|

## 出力

| 関数 | 返却式 | 定義元 |
|---|---|---|
| list_foods | api_functions.list_foods(catalog, q) | backend/src/app/apis/foods/list_foods/router.py:28 |
| list_foods | FoodsResponse(items=items, total=total) | backend/src/app/apis/foods/list_foods/functions.py:8 |
| PostgresCatalog.foods | ([Food.model_validate(row) for row in rows[0]['items']], int(rows[0]['total'])) | backend/src/app/integrations/catalog/postgres_provider.py:18 |

APIとして返す型・status・headerは [インターフェース](interface.md) の実OpenAPIを参照。

## 責務

| 関数 | 処理 | 定義元 |
|---|---|---|
| list_foods | 個別説明なし | backend/src/app/apis/foods/list_foods/router.py:28 |
| list_foods | 入力を正規化し、DBの食品・別名に対して検索する。 | backend/src/app/apis/foods/list_foods/functions.py:8 |
| PostgresCatalog.foods | 個別説明なし | backend/src/app/integrations/catalog/postgres_provider.py:18 |

[SQL](queries.md) / [シーケンス](sequence.md) / [ログ](messages.md) / [要因別テスト](tests.md)
