# インターフェース: entity_recipe_version_update

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`PUT /api/entities/recipe_version/{row_id}` — レシピ内容版の更新

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
| base_servings | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 登録分量が何人前か |
| content_hash | string | 必須 | minLength=64; maxLength=64 | 内容ハッシュ |
| description | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=5000 | 料理の紹介文 |
| output_amount | anyOf(number, string) | 必須 | anyOfの制約=number: exclusiveMinimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 完成量 |
| output_unit_id | string (uuid) | 必須 | 追加制約なし | 完成量単位 |
| published_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 公開日時 |
| recipe_id | string (uuid) | 必須 | 追加制約なし | 所属レシピ |
| release_id | string (uuid) | 必須 | 追加制約なし | 採用カタログ版 |
| status | string | 必須 | enum=["draft", "published", "withdrawn"] | 版の状態 |
| validation | string | 必須 | enum=["pending", "passed", "failed", "needs_review"] | 公開審査 |
| version | integer | 必須 | exclusiveMinimum=0.0 | 版番号 |

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

RecipeVersionRow

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| base_servings | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 登録分量が何人前か |
| content_hash | string | 必須 | minLength=64; maxLength=64 | 内容ハッシュ |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| description | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=5000 | 料理の紹介文 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| output_amount | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 完成量 |
| output_unit_id | string (uuid) | 必須 | 追加制約なし | 完成量単位 |
| published_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 公開日時 |
| recipe_id | string (uuid) | 必須 | 追加制約なし | 所属レシピ |
| release_id | string (uuid) | 必須 | 追加制約なし | 採用カタログ版 |
| status | string | 必須 | enum=["draft", "published", "withdrawn"] | 版の状態 |
| validation | string | 必須 | enum=["pending", "passed", "failed", "needs_review"] | 公開審査 |
| version | integer | 必須 | exclusiveMinimum=0.0 | 版番号 |

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
"""レシピ内容版の更新。具体例は専用型と操作別受入テストに対応する。"""

OPERATION_ID = "entity_recipe_version_update"
TABLE = "recipe_version"
ACTION = "update"
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "レシピ内容版の更新。認証情報は依存から取得し、本人所有または管理者権限を検査する。",
  "operationId": "entity_recipe_version_update",
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
          "$ref": "#/components/schemas/RecipeVersionWrite"
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
            "$ref": "#/components/schemas/RecipeVersionRow"
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
  "summary": "レシピ内容版の更新",
  "tags": [
    "正規化データ: レシピ内容版"
  ]
}
```
