# インターフェース: get_recipe

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/recipes/{recipe_id}` — 料理の材料と工程を表示する

## 認証

[{"HTTPBearer": []}, {}, {"HTTPBearer": []}]

宣言: public

## パラメーター

| 場所 | 名前 | 必須性 | 型 | 制約 | 説明 |
|---|---|---|---|---|---|
| path | recipe_id | 必須 | string (uuid) | 追加制約なし |  |
| query | preview | 任意 | boolean | default=false |  |
| query | versionId | 任意 | anyOf(string (uuid), null) | 追加制約なし |  |

## リクエスト本文

リクエスト本文の定義なし。

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

Recipe

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| arrangementIds | array&lt;string&gt; | 必須 | maxItems=100; 要素の制約=minLength=1; maxLength=128 | Arrangementids |
| description | string | 必須 | maxLength=5000 | Description |
| equipment | array&lt;string&gt; | 必須 | maxItems=50; 要素の制約=maxLength=500 | Equipment |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| imageUrl | anyOf(string, null) | 任意 | anyOfの制約=string: maxLength=500 | Imageurl |
| ingredients | array&lt;RecipeIngredient&gt; | 必須 | maxItems=100 | Ingredients |
| minutes | number | 必須 | minimum=0.0; maximum=1000000.0 | Minutes |
| name | string | 必須 | maxLength=500 | Name |
| publicationStatus | string | 任意 | enum=["draft", "published", "withdrawn"]; default="draft" | Publicationstatus |
| sample | boolean | 必須 | 追加制約なし | Sample |
| servings | number | 必須 | maximum=1000.0; exclusiveMinimum=0.0 | Servings |
| steps | array&lt;RecipeStep&gt; | 必須 | maxItems=100 | Steps |
| tags | array&lt;string&gt; | 必須 | maxItems=100; 要素の制約=maxLength=500 | Tags |
| versionId | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=128 | Versionid |
| withdrawalReason | anyOf(string, null) | 任意 | anyOfの制約=string: maxLength=20000 | Withdrawalreason |

### HTTP 401: 下書き閲覧にはログインが必要

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 403: 下書き閲覧が許可されていない環境

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 404: 料理が見つからない

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
ERRORS = {404: {"detail": "recipe not found"}}
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "operationId": "get_recipe",
  "parameters": [
    {
      "in": "path",
      "name": "recipe_id",
      "required": true,
      "schema": {
        "format": "uuid",
        "title": "Recipe Id",
        "type": "string"
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
    },
    {
      "in": "query",
      "name": "versionId",
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
        "title": "Versionid"
      }
    }
  ],
  "responses": {
    "200": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/Recipe"
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
    "404": {
      "description": "料理が見つからない"
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
  "summary": "料理の材料と工程を表示する"
}
```
