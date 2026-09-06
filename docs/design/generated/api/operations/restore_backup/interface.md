# インターフェース: restore_backup

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/backups/restore` — 確認したバックアップで本人のデータを全置換する

## 認証

[{"HTTPBearer": []}]

宣言: 検証済みBearerトークンと本人所有権

## パラメーター

なし。

## リクエスト本文

必須

### application/json

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| backup | BackupDocument-Input | 必須 | 追加制約なし |  |
| confirmed | boolean | 必須 | const=true | 全置換の最終確認を明示した場合だけtrue |
| expectedVersion | integer | 必須 | minimum=0.0 | Expectedversion |
| intentId | string (uuid) | 必須 | 追加制約なし | Intentid |

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

### HTTP 401: 本人・形式・版・確認・DB制約の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 403: 本人・形式・版・確認・DB制約の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 409: 本人・形式・版・確認・DB制約の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 413: 本人・形式・版・確認・DB制約の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 422: 本人・形式・版・確認・DB制約の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 503: 本人・形式・版・確認・DB制約の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

## 操作のサンプル

```python
"""確認したバックアップで本人のデータを全置換する。本人・版・確認の具体例はバックアップ受入試験に対応する。"""
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "確認したバックアップで本人のデータを全置換する。利用者の確認がない全置換を受け付けない。",
  "operationId": "restore_backup",
  "parameters": [],
  "requestBody": {
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/BackupRestoreRequest"
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
      "description": "本人・形式・版・確認・DB制約の検証失敗"
    },
    "403": {
      "description": "本人・形式・版・確認・DB制約の検証失敗"
    },
    "409": {
      "description": "本人・形式・版・確認・DB制約の検証失敗"
    },
    "413": {
      "description": "本人・形式・版・確認・DB制約の検証失敗"
    },
    "422": {
      "description": "本人・形式・版・確認・DB制約の検証失敗"
    },
    "503": {
      "description": "本人・形式・版・確認・DB制約の検証失敗"
    }
  },
  "security": [
    {
      "HTTPBearer": []
    }
  ],
  "summary": "確認したバックアップで本人のデータを全置換する",
  "tags": [
    "バックアップ"
  ]
}
```
