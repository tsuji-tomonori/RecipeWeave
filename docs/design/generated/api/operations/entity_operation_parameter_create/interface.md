# インターフェース: entity_operation_parameter_create

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/entities/operation_parameter` — 動作パラメータ定義の作成

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
| allowed_values | anyOf(array&lt;string&gt;, null) | 任意 | 追加制約なし | option型の具体値配列 |
| code | string | 必須 | minLength=1; maxLength=20000 | thickness_mm等 |
| max_value | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 許容上限 |
| min_value | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 許容下限 |
| name | string | 必須 | minLength=1; maxLength=20000 | 厚さ等 |
| operation_id | string (uuid) | 必須 | 追加制約なし | 動作 |
| required | boolean | 必須 | 追加制約なし | 必須か |
| unit_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 単位 |
| value_type | string | 必須 | enum=["decimal", "integer", "boolean", "text", "option"] | 値型 |

## レスポンス

### HTTP 201: Successful Response

Content-Type: `application/json`

OperationParameterRow

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| allowed_values | anyOf(array&lt;string&gt;, null) | 必須 | 追加制約なし | option型の具体値配列 |
| code | string | 必須 | minLength=1; maxLength=20000 | thickness_mm等 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| max_value | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 許容上限 |
| min_value | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 許容下限 |
| name | string | 必須 | minLength=1; maxLength=20000 | 厚さ等 |
| operation_id | string (uuid) | 必須 | 追加制約なし | 動作 |
| required | boolean | 必須 | 追加制約なし | 必須か |
| unit_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 単位 |
| value_type | string | 必須 | enum=["decimal", "integer", "boolean", "text", "option"] | 値型 |

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
"""動作パラメータ定義の作成。具体例は専用型と操作別受入テストに対応する。"""

OPERATION_ID = "entity_operation_parameter_create"
TABLE = "operation_parameter"
ACTION = "create"
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "動作パラメータ定義の作成。認証情報は依存から取得し、本人所有または管理者権限を検査する。",
  "operationId": "entity_operation_parameter_create",
  "parameters": [],
  "requestBody": {
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/OperationParameterWrite"
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
            "$ref": "#/components/schemas/OperationParameterRow"
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
  "summary": "動作パラメータ定義の作成",
  "tags": [
    "正規化データ: 動作パラメータ定義"
  ]
}
```
