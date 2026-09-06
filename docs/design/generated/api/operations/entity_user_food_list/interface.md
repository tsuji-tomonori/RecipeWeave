# インターフェース: entity_user_food_list

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/entities/user_food` — 利用者が追加した独自食材の所有の一覧

## 認証

[{"HTTPBearer": []}]

宣言: bearer

## パラメーター

| 場所 | 名前 | 必須性 | 型 | 制約 | 説明 |
|---|---|---|---|---|---|
| query | limit | 任意 | integer | default=50; minimum=1; maximum=100 |  |
| query | after | 任意 | anyOf(string (uuid), null) | 追加制約なし |  |

## リクエスト本文

リクエスト本文の定義なし。

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

array<UserFoodRow>

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| 値全体 | array&lt;UserFoodRow&gt; | — | 追加制約なし |  |

### HTTP 401: 認証が必要

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 403: 操作・参照権限なし

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 409: 同時更新またはDB業務制約違反

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 422: 入力不正

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 503: DB接続不可

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

## 操作のサンプル

```python
# generate_entity_apis.py による自動生成。直接編集しない。
"""利用者が追加した独自食材の所有の一覧。具体例は専用型と操作別受入テストに対応する。"""

OPERATION_ID = "entity_user_food_list"
TABLE = "user_food"
ACTION = "list"
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "利用者が追加した独自食材の所有の一覧。認証情報は依存から取得し、本人所有または管理者権限を検査する。",
  "operationId": "entity_user_food_list",
  "parameters": [
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
      "name": "after",
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
        "title": "After"
      }
    }
  ],
  "responses": {
    "200": {
      "content": {
        "application/json": {
          "schema": {
            "items": {
              "$ref": "#/components/schemas/UserFoodRow"
            },
            "title": "Response Entity User Food List",
            "type": "array"
          }
        }
      },
      "description": "Successful Response"
    },
    "401": {
      "description": "認証が必要"
    },
    "403": {
      "description": "操作・参照権限なし"
    },
    "409": {
      "description": "同時更新またはDB業務制約違反"
    },
    "422": {
      "description": "入力不正"
    },
    "503": {
      "description": "DB接続不可"
    }
  },
  "security": [
    {
      "HTTPBearer": []
    }
  ],
  "summary": "利用者が追加した独自食材の所有の一覧",
  "tags": [
    "正規化データ: 利用者が追加した独自食材の所有"
  ]
}
```
