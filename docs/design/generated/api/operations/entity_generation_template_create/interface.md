# インターフェース: entity_generation_template_create

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/entities/generation_template` — 列挙テンプレート版の作成

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
| candidate_count | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | この定義の正確な設計点数 |
| code | string | 必須 | minLength=1; maxLength=20000 | テンプレートコード |
| contract | GenerationTemplateContract | 必須 | 追加制約なし | 主副材の許可集合・k・味付・経路 |
| contract_hash | string | 必須 | minLength=64; maxLength=64 | 定義ハッシュ |
| release_id | string (uuid) | 必須 | 追加制約なし | カタログ版 |
| version | integer | 必須 | exclusiveMinimum=0.0 | 定義版 |

## レスポンス

### HTTP 201: Successful Response

Content-Type: `application/json`

GenerationTemplateRow

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| candidate_count | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | この定義の正確な設計点数 |
| code | string | 必須 | minLength=1; maxLength=20000 | テンプレートコード |
| contract | GenerationTemplateContract | 必須 | 追加制約なし | 主副材の許可集合・k・味付・経路 |
| contract_hash | string | 必須 | minLength=64; maxLength=64 | 定義ハッシュ |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変ID |
| release_id | string (uuid) | 必須 | 追加制約なし | カタログ版 |
| version | integer | 必須 | exclusiveMinimum=0.0 | 定義版 |

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
"""列挙テンプレート版の作成。具体例は専用型と操作別受入テストに対応する。"""

OPERATION_ID = "entity_generation_template_create"
TABLE = "generation_template"
ACTION = "create"
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "列挙テンプレート版の作成。認証情報は依存から取得し、本人所有または管理者権限を検査する。",
  "operationId": "entity_generation_template_create",
  "parameters": [],
  "requestBody": {
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/GenerationTemplateWrite"
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
            "$ref": "#/components/schemas/GenerationTemplateRow"
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
  "summary": "列挙テンプレート版の作成",
  "tags": [
    "正規化データ: 列挙テンプレート版"
  ]
}
```
