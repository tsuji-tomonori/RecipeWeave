---
title: "インターフェース: get_state"
---

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/state` — 認証した利用者自身の状態を読む

## 認証

[{"HTTPBearer": []}]

宣言: cognito-access-jwt

## パラメーター

なし。

## リクエスト本文

リクエスト本文の定義なし。

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

### HTTP 503: 同期を利用できない

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

## 操作のサンプル

```python
SUCCESS = {"version": 0, "snapshot": None}
ERRORS = {401: {"detail": "access token required"}, 503: {"detail": "service unavailable"}}
```

[共有モデルの全仕様](/RecipeWeave/quality/design/api/models/) / [共通エラー](/RecipeWeave/quality/design/api/errors/)

## このAPIのOpenAPI定義

```json
{
  "operationId": "get_state",
  "parameters": [],
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
    "503": {
      "description": "同期を利用できない"
    }
  },
  "security": [
    {
      "HTTPBearer": []
    }
  ],
  "summary": "認証した利用者自身の状態を読む"
}
```
