# インターフェース: entity_receipt_line_create

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/entities/receipt_line` — レシートの商品候補と確定した在庫の対応の作成

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
| amount | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 数量。不明はNULL |
| decision | string | 必須 | enum=["accepted", "skipped", "unresolved"] | accepted/skipped/unresolved |
| form_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 確定した食材形態 |
| import_id | string (uuid) | 必須 | 追加制約なし | レシート処理 |
| line_no | integer | 必須 | exclusiveMinimum=0.0 | レシート内の表示順 |
| pantry_lot_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 登録したロット |
| product_version_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 確定した商品版 |
| raw_name | string | 必須 | minLength=1; maxLength=20000 | 利用者が確認できる商品原表記 |
| unit_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 確定数量の単位 |

## レスポンス

### HTTP 201: Successful Response

Content-Type: `application/json`

ReceiptLineRow

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 数量。不明はNULL |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| decision | string | 必須 | enum=["accepted", "skipped", "unresolved"] | accepted/skipped/unresolved |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| form_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 確定した食材形態 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| import_id | string (uuid) | 必須 | 追加制約なし | レシート処理 |
| line_no | integer | 必須 | exclusiveMinimum=0.0 | レシート内の表示順 |
| pantry_lot_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 登録したロット |
| product_version_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 確定した商品版 |
| raw_name | string | 必須 | minLength=1; maxLength=20000 | 利用者が確認できる商品原表記 |
| unit_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 確定数量の単位 |

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
"""レシートの商品候補と確定した在庫の対応の作成。具体例は専用型と操作別受入テストに対応する。"""

OPERATION_ID = "entity_receipt_line_create"
TABLE = "receipt_line"
ACTION = "create"
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "レシートの商品候補と確定した在庫の対応の作成。認証情報は依存から取得し、本人所有または管理者権限を検査する。",
  "operationId": "entity_receipt_line_create",
  "parameters": [],
  "requestBody": {
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/ReceiptLineWrite"
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
            "$ref": "#/components/schemas/ReceiptLineRow"
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
  "summary": "レシートの商品候補と確定した在庫の対応の作成",
  "tags": [
    "正規化データ: レシートの商品候補と確定した在庫の対応"
  ]
}
```
