# インターフェース: put_state

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`PUT /api/state` — 版を確認して利用者自身の状態を置き換える

## 認証

[{"HTTPBearer": []}]

宣言: cognito-access-jwt

## パラメーター

なし。

## リクエスト本文

必須

### application/json

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| expectedVersion | integer | 必須 | minimum=0.0; maximum=9.223372036854776e+18 | Expectedversion |
| snapshot | AppSnapshot | 必須 | 追加制約なし |  |

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

StateEnvelope

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| snapshot | anyOf(AppSnapshot, null) | 必須 | 追加制約なし |  |
| version | integer | 必須 | minimum=0.0 | Version |

### HTTP 401: 有効なアクセストークンが必要

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 409: 版が競合したため、再読込後にやり直す

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 413: リクエストが1MiBを超えている

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 422: Validation Error

Content-Type: `application/json`

HTTPValidationError

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| detail | array&lt;ValidationError&gt; | 任意 | 追加制約なし | Detail |

### HTTP 503: 同期を利用できない

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

## 操作のサンプル

```python
ERRORS = {409: {"detail": "state version conflict"}, 413: {"detail": "request too large"}}
```

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "operationId": "put_state",
  "parameters": [],
  "requestBody": {
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/PutStateRequest"
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
            "$ref": "#/components/schemas/StateEnvelope"
          }
        }
      },
      "description": "Successful Response"
    },
    "401": {
      "description": "有効なアクセストークンが必要"
    },
    "409": {
      "description": "版が競合したため、再読込後にやり直す"
    },
    "413": {
      "description": "リクエストが1MiBを超えている"
    },
    "422": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/HTTPValidationError"
          }
        }
      },
      "description": "Validation Error"
    },
    "503": {
      "description": "同期を利用できない"
    }
  },
  "security": [
    {
      "HTTPBearer": []
    }
  ],
  "summary": "版を確認して利用者自身の状態を置き換える"
}
```
