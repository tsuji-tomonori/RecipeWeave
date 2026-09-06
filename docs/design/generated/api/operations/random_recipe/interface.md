# インターフェース: random_recipe

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/recipes/random` — 保存済みの料理から一品を選ぶ

## 認証

[{"HTTPBearer": []}, {}, {"HTTPBearer": []}]

宣言: public; previewには開発環境の認証が必要

## パラメーター

| 場所 | 名前 | 必須性 | 型 | 制約 | 説明 |
|---|---|---|---|---|---|
| query | excludeId | 任意 | anyOf(string (uuid), null) | 追加制約なし |  |
| query | excludedFoodIds | 任意 | array&lt;string (uuid)&gt; | maxItems=100 |  |
| query | preview | 任意 | boolean | default=false |  |

## リクエスト本文

リクエスト本文の定義なし。

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

RandomRecipeResponse

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| item | anyOf(Recipe, null) | 必須 | 追加制約なし |  |
| total | integer | 必須 | 追加制約なし | Total |

### HTTP 401: 下書き閲覧にはログインが必要

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 403: 下書き閲覧が許可されていない環境

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 422: Validation Error

Content-Type: `application/json`

HTTPValidationError

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| detail | array&lt;ValidationError&gt; | 任意 | 追加制約なし | Detail |

### HTTP 503: DB接続が利用できない

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

## 操作のサンプル

```python
"""候補なしを、架空の料理で補わず返す。"""

EMPTY_RESPONSE = {"item": None, "total": 0}
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "operationId": "random_recipe",
  "parameters": [
    {
      "in": "query",
      "name": "excludeId",
      "required": false,
      "schema": {
        "anyOf": [
          {
            "format": "uuid",
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "title": "Excludeid"
      }
    },
    {
      "in": "query",
      "name": "excludedFoodIds",
      "required": false,
      "schema": {
        "items": {
          "format": "uuid",
          "type": "string"
        },
        "maxItems": 100,
        "title": "Excludedfoodids",
        "type": "array"
      }
    },
    {
      "in": "query",
      "name": "preview",
      "required": false,
      "schema": {
        "default": false,
        "title": "Preview",
        "type": "boolean"
      }
    }
  ],
  "responses": {
    "200": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/RandomRecipeResponse"
          }
        }
      },
      "description": "Successful Response"
    },
    "401": {
      "description": "下書き閲覧にはログインが必要"
    },
    "403": {
      "description": "下書き閲覧が許可されていない環境"
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
      "description": "DB接続が利用できない"
    }
  },
  "security": [
    {
      "HTTPBearer": []
    },
    {},
    {
      "HTTPBearer": []
    }
  ],
  "summary": "保存済みの料理から一品を選ぶ"
}
```
