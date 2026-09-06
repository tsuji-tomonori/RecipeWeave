# インターフェース: list_recipes

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/recipes` — 食材・時間から保存済みの料理を探す

## 認証

[{"HTTPBearer": []}, {}, {"HTTPBearer": []}]

宣言: public

## パラメーター

| 場所 | 名前 | 必須性 | 型 | 制約 | 説明 |
|---|---|---|---|---|---|
| query | q | 任意 | string | default=""; maxLength=100 |  |
| query | selectedFoodIds | 任意 | array&lt;string (uuid)&gt; | maxItems=100 |  |
| query | excludedFoodIds | 任意 | array&lt;string (uuid)&gt; | maxItems=100 |  |
| query | match | 任意 | string | enum=["all", "any"]; default="all" |  |
| query | maxMinutes | 任意 | anyOf(number, null) | anyOfの制約=number: maximum=1440; exclusiveMinimum=0 |  |
| query | equipment | 任意 | array&lt;string&gt; | maxItems=50 |  |
| query | limit | 任意 | integer | default=50; minimum=1; maximum=100 |  |
| query | offset | 任意 | integer | default=0; minimum=0; maximum=1000000 |  |
| query | preview | 任意 | boolean | default=false |  |

## リクエスト本文

リクエスト本文の定義なし。

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

RecipesResponse

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| items | array&lt;Recipe&gt; | 必須 | 追加制約なし | Items |
| limit | integer | 必須 | 追加制約なし | Limit |
| offset | integer | 必須 | 追加制約なし | Offset |
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
SUCCESS: dict[str, object] = {"items": [], "total": 0, "sample": True}
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "operationId": "list_recipes",
  "parameters": [
    {
      "in": "query",
      "name": "q",
      "required": false,
      "schema": {
        "default": "",
        "maxLength": 100,
        "title": "Q",
        "type": "string"
      }
    },
    {
      "in": "query",
      "name": "selectedFoodIds",
      "required": false,
      "schema": {
        "items": {
          "format": "uuid",
          "type": "string"
        },
        "maxItems": 100,
        "title": "Selectedfoodids",
        "type": "array"
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
      "name": "match",
      "required": false,
      "schema": {
        "default": "all",
        "enum": [
          "all",
          "any"
        ],
        "title": "Match",
        "type": "string"
      }
    },
    {
      "in": "query",
      "name": "maxMinutes",
      "required": false,
      "schema": {
        "anyOf": [
          {
            "exclusiveMinimum": 0,
            "maximum": 1440,
            "type": "number"
          },
          {
            "type": "null"
          }
        ],
        "title": "Maxminutes"
      }
    },
    {
      "in": "query",
      "name": "equipment",
      "required": false,
      "schema": {
        "items": {
          "type": "string"
        },
        "maxItems": 50,
        "title": "Equipment",
        "type": "array"
      }
    },
    {
      "in": "query",
      "name": "limit",
      "required": false,
      "schema": {
        "default": 50,
        "maximum": 100,
        "minimum": 1,
        "title": "Limit",
        "type": "integer"
      }
    },
    {
      "in": "query",
      "name": "offset",
      "required": false,
      "schema": {
        "default": 0,
        "maximum": 1000000,
        "minimum": 0,
        "title": "Offset",
        "type": "integer"
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
            "$ref": "#/components/schemas/RecipesResponse"
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
  "summary": "食材・時間から保存済みの料理を探す"
}
```
