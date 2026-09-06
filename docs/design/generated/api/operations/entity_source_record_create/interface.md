# インターフェース: entity_source_record_create

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/entities/source_record` — 根拠資料の作成

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
| content_hash | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=64; maxLength=64 | 参照内容のハッシュ |
| license_note | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=20000 | 利用条件・権利確認 |
| locator | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=20000 | 資料内位置 |
| retrieved_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 取得時点 |
| title | string | 必須 | minLength=1; maxLength=20000 | 根拠名 |
| url | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=20000 | 公式資料URL |

## レスポンス

### HTTP 201: Successful Response

Content-Type: `application/json`

SourceRecordRow

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| content_hash | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=64; maxLength=64 | 参照内容のハッシュ |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| license_note | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=20000 | 利用条件・権利確認 |
| locator | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=20000 | 資料内位置 |
| retrieved_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 取得時点 |
| title | string | 必須 | minLength=1; maxLength=20000 | 根拠名 |
| url | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=20000 | 公式資料URL |

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
"""根拠資料の作成。具体例は専用型と操作別受入テストに対応する。"""

OPERATION_ID = "entity_source_record_create"
TABLE = "source_record"
ACTION = "create"
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "根拠資料の作成。認証情報は依存から取得し、本人所有または管理者権限を検査する。",
  "operationId": "entity_source_record_create",
  "parameters": [],
  "requestBody": {
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/SourceRecordWrite"
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
            "$ref": "#/components/schemas/SourceRecordRow"
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
  "summary": "根拠資料の作成",
  "tags": [
    "正規化データ: 根拠資料"
  ]
}
```
