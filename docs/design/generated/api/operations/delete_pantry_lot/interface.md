# インターフェース: delete_pantry_lot

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`DELETE /api/pantry-lots/{row_id}` — 手持ち食材を削除する

## 認証

[{"HTTPBearer": []}]

宣言: 検証済みBearerトークンと本人所有権

## パラメーター

| 場所 | 名前 | 必須性 | 型 | 制約 | 説明 |
|---|---|---|---|---|---|
| path | row_id | 必須 | string (uuid) | 追加制約なし |  |

## リクエスト本文

必須

### application/json

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| expectedVersion | integer | 必須 | minimum=0.0; maximum=9007199254740990.0 | Expectedversion |

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

AppSnapshot

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| cooking | anyOf(CookingSession, null) | 必須 | 追加制約なし |  |
| customFoods | array&lt;Food&gt; | 必須 | maxItems=1000 | Customfoods |
| drafts | object | 必須 | additionalProperties={"$ref": "#/components/schemas/RecipeDraft"} | Drafts |
| imports | array&lt;ReceiptImport&gt; | 必須 | maxItems=1000 | Imports |
| lots | array&lt;StockLot&gt; | 必須 | maxItems=5000 | Lots |
| meal | array&lt;MealItem&gt; | 必須 | maxItems=50 | Meal |
| saved | array&lt;string&gt; | 必須 | maxItems=10000; 要素の制約=minLength=1; maxLength=128 | Saved |
| schemaVersion | integer | 必須 | const=1 | Schemaversion |
| search | SearchFilters | 必須 | 追加制約なし |  |
| settings | Settings | 必須 | 追加制約なし |  |
| shoppingChecks | array&lt;ShoppingCheck&gt; | 必須 | maxItems=1000 | Shoppingchecks |
| version | integer | 必須 | minimum=0.0 | Version |

### HTTP 401: 認証・所有権・版・入力の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 403: 認証・所有権・版・入力の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 404: 認証・所有権・版・入力の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 409: 認証・所有権・版・入力の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 422: 認証・所有権・版・入力の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 503: 認証・所有権・版・入力の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

## 操作のサンプル

```python
SUCCESS = {"説明": "本人の最新ワークスペースを返す。DB値から構築する。"}
ERRORS = {401: {"detail": "ログインが必要です"}, 409: {"detail": "他の画面で更新されています"}}
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "手持ち食材を削除する。呼出元が送った利用者IDは使用しない。",
  "operationId": "delete_pantry_lot",
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
  "requestBody": {
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/RevisionRequest"
        }
      }
    },
    "required": true
  },
  "responses": {
    "200": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/AppSnapshot"
          }
        }
      },
      "description": "Successful Response"
    },
    "401": {
      "description": "認証・所有権・版・入力の検証失敗"
    },
    "403": {
      "description": "認証・所有権・版・入力の検証失敗"
    },
    "404": {
      "description": "認証・所有権・版・入力の検証失敗"
    },
    "409": {
      "description": "認証・所有権・版・入力の検証失敗"
    },
    "422": {
      "description": "認証・所有権・版・入力の検証失敗"
    },
    "503": {
      "description": "認証・所有権・版・入力の検証失敗"
    }
  },
  "security": [
    {
      "HTTPBearer": []
    }
  ],
  "summary": "手持ち食材を削除する",
  "tags": [
    "利用者の操作"
  ]
}
```
