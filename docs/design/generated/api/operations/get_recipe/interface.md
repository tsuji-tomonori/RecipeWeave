# インターフェース: get_recipe

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/recipes/{recipe_id}` — 料理の材料と工程を表示する

## 認証

[]

宣言: public

## パラメーター

| 場所 | 名前 | 必須性 | 型 | 制約 | 説明 |
|---|---|---|---|---|---|
| path | recipe_id | 必須 | string | maxLength=128 |  |

## リクエスト本文

リクエスト本文の定義なし。

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

Recipe

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| arrangementIds | array&lt;string&gt; | 必須 | maxItems=100 | Arrangementids |
| description | string | 必須 | maxLength=5000 | Description |
| equipment | array&lt;string&gt; | 必須 | maxItems=50 | Equipment |
| id | string | 必須 | minLength=1; maxLength=128 | Id |
| ingredients | array&lt;RecipeIngredient&gt; | 必須 | maxItems=100 | Ingredients |
| minutes | number | 必須 | minimum=0.0; maximum=1000000.0 | Minutes |
| name | string | 必須 | maxLength=500 | Name |
| sample | boolean | 必須 | const=true | Sample |
| servings | number | 必須 | maximum=1000.0; exclusiveMinimum=0.0 | Servings |
| steps | array&lt;RecipeStep&gt; | 必須 | maxItems=100 | Steps |
| tags | array&lt;string&gt; | 必須 | maxItems=100 | Tags |

### HTTP 404: 料理が見つからない

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 422: Validation Error

Content-Type: `application/json`

HTTPValidationError

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| detail | array&lt;ValidationError&gt; | 任意 | 追加制約なし | Detail |

## 操作のサンプル

```python
ERRORS = {404: {"detail": "recipe not found"}}
```

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
        "maxLength": 128,
        "title": "Recipe Id",
        "type": "string"
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
    }
  },
  "summary": "料理の材料と工程を表示する"
}
```
