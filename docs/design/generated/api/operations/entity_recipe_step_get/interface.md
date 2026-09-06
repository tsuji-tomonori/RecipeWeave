# インターフェース: entity_recipe_step_get

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/entities/recipe_step/{row_id}` — 調理工程節点の取得

## 認証

[{"HTTPBearer": []}]

宣言: bearer

## パラメーター

| 場所 | 名前 | 必須性 | 型 | 制約 | 説明 |
|---|---|---|---|---|---|
| path | row_id | 必須 | string (uuid) | 追加制約なし |  |

## リクエスト本文

リクエスト本文の定義なし。

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

RecipeStepRow

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| attention | string | 必須 | enum=["active", "monitored", "passive"] | 作業者拘束 |
| completion_cue | string | 必須 | minLength=1; maxLength=20000 | 実測・目視の終了条件 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| duration_max_s | integer | 必須 | 追加制約なし | 所要秒上限 |
| duration_min_s | integer | 必須 | minimum=0.0 | 所要秒下限 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| instruction | string | 必須 | minLength=1; maxLength=5000 | 個別補足 |
| operation_id | string (uuid) | 必須 | 追加制約なし | 標準動作 |
| recipe_version_id | string (uuid) | 必須 | 追加制約なし | 所属版 |
| scaling_rule_id | string (uuid) | 必須 | 追加制約なし | 時間の人数変更規則 |
| step_no | integer | 必須 | exclusiveMinimum=0.0 | 表示順(依存順とは別) |
| title | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=500 | 工程の短い見出し |

### HTTP 401: 認証が必要

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 403: 操作・参照権限なし

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 404: 対象なし

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
"""調理工程節点の取得。具体例は専用型と操作別受入テストに対応する。"""

OPERATION_ID = "entity_recipe_step_get"
TABLE = "recipe_step"
ACTION = "get"
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "調理工程節点の取得。認証情報は依存から取得し、本人所有または管理者権限を検査する。",
  "operationId": "entity_recipe_step_get",
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
    }
  ],
  "responses": {
    "200": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/RecipeStepRow"
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
    "404": {
      "description": "対象なし"
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
  "summary": "調理工程節点の取得",
  "tags": [
    "正規化データ: 調理工程節点"
  ]
}
```
