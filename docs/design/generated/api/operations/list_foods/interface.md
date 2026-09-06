# インターフェース: list_foods

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/foods` — 食材候補を検索する

## 認証

[{"HTTPBearer": []}, {}, {"HTTPBearer": []}]

宣言: public

## パラメーター

| 場所 | 名前 | 必須性 | 型 | 制約 | 説明 |
|---|---|---|---|---|---|
| query | q | 任意 | string | default=""; maxLength=100 |  |

## リクエスト本文

リクエスト本文の定義なし。

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

FoodsResponse

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| items | array&lt;Food&gt; | 必須 | 追加制約なし | Items |
| total | integer | 必須 | 追加制約なし | Total |

### HTTP 401: 指定された認証情報が無効

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
SUCCESS: dict[str, object] = {"items": [], "total": 0}
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "operationId": "list_foods",
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
    }
  ],
  "responses": {
    "200": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/FoodsResponse"
          }
        }
      },
      "description": "Successful Response"
    },
    "401": {
      "description": "指定された認証情報が無効"
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
  "summary": "食材候補を検索する"
}
```
