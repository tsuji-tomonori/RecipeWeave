# インターフェース: entity_user_recipe_event_create

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/entities/user_recipe_event` — 提案・調理履歴の作成

## 認証

[{"HTTPBearer": []}]

宣言: bearer

## パラメーター

なし。

## リクエスト本文

必須

### application/json

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| kind | string | 必須 | enum=["shown", "cooked", "liked", "disliked"] | 提示/調理/評価 |
| occurred_at | string (date-time) | 必須 | 追加制約なし | 発生時刻 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 提案版 |
| request_key | string | 必須 | minLength=1; maxLength=20000 | リクエスト識別子 |
| user_id | string (uuid) | 必須 | 追加制約なし | 利用者 |

## レスポンス

### HTTP 201: Successful Response

Content-Type: `application/json`

UserRecipeEventRow

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| kind | string | 必須 | enum=["shown", "cooked", "liked", "disliked"] | 提示/調理/評価 |
| occurred_at | string (date-time) | 必須 | 追加制約なし | 発生時刻 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 提案版 |
| request_key | string | 必須 | minLength=1; maxLength=20000 | リクエスト識別子 |
| user_id | string (uuid) | 必須 | 追加制約なし | 利用者 |

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
"""提案・調理履歴の作成。具体例は専用型と操作別受入テストに対応する。"""

OPERATION_ID = "entity_user_recipe_event_create"
TABLE = "user_recipe_event"
ACTION = "create"
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "提案・調理履歴の作成。認証情報は依存から取得し、本人所有または管理者権限を検査する。",
  "operationId": "entity_user_recipe_event_create",
  "parameters": [],
  "requestBody": {
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/UserRecipeEventWrite"
        }
      }
    },
    "required": true
  },
  "responses": {
    "201": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/UserRecipeEventRow"
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
  "summary": "提案・調理履歴の作成",
  "tags": [
    "正規化データ: 提案・調理履歴"
  ]
}
```
