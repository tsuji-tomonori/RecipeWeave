# インターフェース: entity_app_user_update

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`PUT /api/entities/app_user/{row_id}` — アプリ利用者の更新

## 認証

[{"HTTPBearer": []}]

宣言: bearer

## パラメーター

| 場所 | 名前 | 必須性 | 型 | 制約 | 説明 |
|---|---|---|---|---|---|
| path | row_id | 必須 | string (uuid) | 追加制約なし |  |
| header | If-Match | 任意 | anyOf(string, null) | 追加制約なし |  |

## リクエスト本文

必須

### application/json

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| locale | string | 必須 | minLength=1; maxLength=20000 | 表示言語 |
| timezone | string | 必須 | minLength=1; maxLength=20000 | IANAタイムゾーン |

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

AppUserRow

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| auth_subject | string | 必須 | minLength=1; maxLength=20000 | 認証基盤の不透明識別子 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| locale | string | 必須 | minLength=1; maxLength=20000 | 表示言語 |
| state | string | 必須 | enum=["active", "erasure_pending"] | 利用/削除処理 |
| timezone | string | 必須 | minLength=1; maxLength=20000 | IANAタイムゾーン |

### HTTP 401: 認証が必要

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 403: 操作・参照権限なし

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 409: 同時更新またはDB業務制約違反

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 422: 入力不正

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 428: If-Matchが必要

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 503: DB接続不可

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

## 操作のサンプル

```python
# generate_entity_apis.py による自動生成。直接編集しない。
"""アプリ利用者の更新。具体例は専用型と操作別受入テストに対応する。"""

OPERATION_ID = "entity_app_user_update"
TABLE = "app_user"
ACTION = "update"
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "アプリ利用者の更新。認証情報は依存から取得し、本人所有または管理者権限を検査する。",
  "operationId": "entity_app_user_update",
  "parameters": [
    {
      "in": "path",
      "name": "row_id",
      "required": true,
      "schema": {
        "format": "uuid",
        "title": "Row Id",
        "type": "string"
      }
    },
    {
      "in": "header",
      "name": "If-Match",
      "required": false,
      "schema": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "title": "If-Match"
      }
    }
  ],
  "requestBody": {
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/AppUserWrite"
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
            "$ref": "#/components/schemas/AppUserRow"
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
    "428": {
      "description": "If-Matchが必要"
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
  "summary": "アプリ利用者の更新",
  "tags": [
    "正規化データ: アプリ利用者"
  ]
}
```
