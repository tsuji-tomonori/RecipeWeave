# インターフェース: local_login

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/auth/local-login` — 開発環境へログインする

## 認証

[]

宣言: public; 開発環境限定。本文の資格情報を検証

## パラメーター

なし。

## リクエスト本文

必須

### application/json

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| password | string | 必須 | minLength=1; maxLength=200 | Password |
| username | string | 必須 | minLength=1; maxLength=50 | Username |

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

LoginResponse

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| access_token | string | 必須 | 追加制約なし | Access Token |
| token_type | string | 任意 | default="bearer" | Token Type |
| user | UserProfile | 必須 | 追加制約なし |  |

### HTTP 401: 認証または設定の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 404: 認証または設定の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 422: 認証または設定の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 503: 認証または設定の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

## 操作のサンプル

```python
SUCCESS = {"説明": "本人の表示名とIDを返す"}
ERRORS = {401: {"detail": "ログイン情報が無効です"}}
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "開発環境へログインする。",
  "operationId": "local_login",
  "parameters": [],
  "requestBody": {
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/LoginRequest"
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
            "$ref": "#/components/schemas/LoginResponse"
          }
        }
      },
      "description": "Successful Response"
    },
    "401": {
      "description": "認証または設定の検証失敗"
    },
    "404": {
      "description": "認証または設定の検証失敗"
    },
    "422": {
      "description": "認証または設定の検証失敗"
    },
    "503": {
      "description": "認証または設定の検証失敗"
    }
  },
  "summary": "開発環境へログインする",
  "tags": [
    "認証"
  ]
}
```
