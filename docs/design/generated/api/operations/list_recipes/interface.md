# インターフェース: list_recipes

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/recipes` — 食材・時間からサンプル料理を探す

## 認証

[]

宣言: public

## パラメーター

| 場所 | 名前 | 必須性 | 型 | 制約 | 説明 |
|---|---|---|---|---|---|
| query | q | 任意 | string | default=""; maxLength=100 |  |
| query | selectedFoodIds | 任意 | array&lt;string&gt; | maxItems=100 |  |
| query | excludedFoodIds | 任意 | array&lt;string&gt; | maxItems=100 |  |
| query | match | 任意 | string | enum=["all", "any"]; default="all" |  |
| query | maxMinutes | 任意 | anyOf(number, null) | 追加制約なし |  |
| query | equipment | 任意 | array&lt;string&gt; | maxItems=50 |  |

## リクエスト本文

リクエスト本文の定義なし。

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

RecipesResponse

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| items | array&lt;Recipe&gt; | 必須 | 追加制約なし | Items |
| sample | boolean | 任意 | const=true; default=true | Sample |
| total | integer | 必須 | 追加制約なし | Total |

### HTTP 422: Validation Error

Content-Type: `application/json`

HTTPValidationError

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| detail | array&lt;ValidationError&gt; | 任意 | 追加制約なし | Detail |

## 操作のサンプル

```python
SUCCESS: dict[str, object] = {"items": [], "total": 0, "sample": True}
```

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
  "summary": "食材・時間からサンプル料理を探す"
}
```
