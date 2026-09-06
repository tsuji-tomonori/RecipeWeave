# インターフェース: get_me

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/me` — 本人のプロフィールを取得する

## 認証

[{"HTTPBearer": []}]

宣言: 検証済みBearerトークン

## パラメーター

なし。

## リクエスト本文

リクエスト本文の定義なし。

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

UserProfile

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| display_name | string | 必須 | 追加制約なし | Display Name |
| id | string | 必須 | 追加制約なし | Id |
| role | string | 必須 | 追加制約なし | Role |

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
  "description": "本人のプロフィールを取得する。",
  "operationId": "get_me",
  "parameters": [],
  "responses": {
    "200": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/UserProfile"
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
  "security": [
    {
      "HTTPBearer": []
    }
  ],
  "summary": "本人のプロフィールを取得する",
  "tags": [
    "認証"
  ]
}
```
