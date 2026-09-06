# インターフェース: entity_shopping_item_create

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/entities/shopping_item` — 買い物行の作成

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
| archived | boolean | 必須 | 追加制約なし | 完了した買い物の保管状態 |
| checked | boolean | 必須 | 追加制約なし | 購入済み |
| checked_at | anyOf(string (date-time), null) | 任意 | 追加制約なし | 購入確認日時 |
| client_key | anyOf(string, null) | 任意 | anyOfの制約=string: minLength=1; maxLength=20000 | 画面操作の安定キー |
| net_shortage | anyOf(number, string) | 必須 | anyOfの制約=number: minimum=0.0 / string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 在庫控除後の不足量 |
| package_count | anyOf(integer, null) | 任意 | 追加制約なし | 購入包装数 |
| product_version_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | 購入SKU |
| session_id | string (uuid) | 必須 | 追加制約なし | 対象調理 |
| surplus_amount | anyOf(number, string, null) | 任意 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 購入後余剰 |
| total_id | string (uuid) | 必須 | 追加制約なし | 需要行 |

## レスポンス

### HTTP 201: Successful Response

Content-Type: `application/json`

ShoppingItemRow

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| archived | boolean | 必須 | 追加制約なし | 完了した買い物の保管状態 |
| checked | boolean | 必須 | 追加制約なし | 購入済み |
| checked_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 購入確認日時 |
| client_key | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=20000 | 画面操作の安定キー |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| net_shortage | string | 必須 | pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 在庫控除後の不足量 |
| package_count | anyOf(integer, null) | 必須 | 追加制約なし | 購入包装数 |
| product_version_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 購入SKU |
| session_id | string (uuid) | 必須 | 追加制約なし | 対象調理 |
| surplus_amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 購入後余剰 |
| total_id | string (uuid) | 必須 | 追加制約なし | 需要行 |

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
"""買い物行の作成。具体例は専用型と操作別受入テストに対応する。"""

OPERATION_ID = "entity_shopping_item_create"
TABLE = "shopping_item"
ACTION = "create"
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "買い物行の作成。認証情報は依存から取得し、本人所有または管理者権限を検査する。",
  "operationId": "entity_shopping_item_create",
  "parameters": [],
  "requestBody": {
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/ShoppingItemWrite"
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
            "$ref": "#/components/schemas/ShoppingItemRow"
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
  "summary": "買い物行の作成",
  "tags": [
    "正規化データ: 買い物行"
  ]
}
```
