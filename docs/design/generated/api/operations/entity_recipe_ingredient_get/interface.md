# インターフェース: entity_recipe_ingredient_get

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/entities/recipe_ingredient/{row_id}` — レシピ材料明細の取得

## 認証

[{"HTTPBearer": []}]

宣言: bearer

## パラメーター

| 場所 | 名前 | 必須性 | 型 | 制約 | 説明 |
|---|---|---|---|---|---|
| path | row_id | 必須 | string (uuid) | 追加制約なし |  |

## リクエスト本文

リクエスト本文の定義なし。

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

RecipeIngredientRow

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 確定値または範囲下限 |
| amount_max | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 範囲上限 |
| amount_mode | string | 必須 | enum=["exact", "range", "to_taste"] | 確定/範囲/適量 |
| canonical_amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 登録版の基準量 |
| component_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | セット内構成品を使う場合 |
| conversion_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 非基準単位の換算根拠 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| demand_kind | string | 必須 | enum=["purchase", "utility", "kit_component"] | 購入対象区分 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| form_id | string (uuid) | 必須 | 追加制約なし | 使用形態 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| kit_parent_line_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 購入対象となるセットの親行 |
| line_no | integer | 必須 | exclusiveMinimum=0.0 | 表示順 |
| note | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=500 | 材料の補足 |
| optional | boolean | 必須 | 追加制約なし | 任意追加材料 |
| product_version_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 商品指定時の仕様版 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 親版 |
| role | string | 必須 | enum=["main", "support", "seasoning", "aroma", "texture", "garnish", "medium"] | 料理での役割 |
| scaling_rule_id | string (uuid) | 必須 | 追加制約なし | 人数変換規則 |
| unit_id | string (uuid) | 必須 | 追加制約なし | 登録単位 |

### HTTP 401: 認証が必要

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 403: 操作・参照権限なし

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 404: 対象なし

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 409: 同時更新またはDB業務制約違反

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 422: 入力不正

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 503: DB接続不可

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

## 操作のサンプル

```python
# generate_entity_apis.py による自動生成。直接編集しない。
"""レシピ材料明細の取得。具体例は専用型と操作別受入テストに対応する。"""

OPERATION_ID = "entity_recipe_ingredient_get"
TABLE = "recipe_ingredient"
ACTION = "get"
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "レシピ材料明細の取得。認証情報は依存から取得し、本人所有または管理者権限を検査する。",
  "operationId": "entity_recipe_ingredient_get",
  "parameters": [
    {
      "in": "path",
      "name": "row_id",
      "required": true,
      "schema": {
        "format": "uuid",
        "title": "Row Id",
        "type": "string"
      }
    }
  ],
  "responses": {
    "200": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/RecipeIngredientRow"
          }
        }
      },
      "description": "Successful Response"
    },
    "401": {
      "description": "認証が必要"
    },
    "403": {
      "description": "操作・参照権限なし"
    },
    "404": {
      "description": "対象なし"
    },
    "409": {
      "description": "同時更新またはDB業務制約違反"
    },
    "422": {
      "description": "入力不正"
    },
    "503": {
      "description": "DB接続不可"
    }
  },
  "security": [
    {
      "HTTPBearer": []
    }
  ],
  "summary": "レシピ材料明細の取得",
  "tags": [
    "正規化データ: レシピ材料明細"
  ]
}
```
