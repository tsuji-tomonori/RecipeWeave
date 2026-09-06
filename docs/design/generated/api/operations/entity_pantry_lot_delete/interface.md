# インターフェース: entity_pantry_lot_delete

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`DELETE /api/entities/pantry_lot/{row_id}` — 手持ち食材ロットの削除

## 認証

[{"HTTPBearer": []}]

宣言: bearer

## パラメーター

| 場所 | 名前 | 必須性 | 型 | 制約 | 説明 |
|---|---|---|---|---|---|
| path | row_id | 必須 | string (uuid) | 追加制約なし |  |
| header | If-Match | 任意 | anyOf(string, null) | 追加制約なし |  |

## リクエスト本文

リクエスト本文の定義なし。

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

PantryLotRow

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 残量 |
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時(UTC) |
| edited | boolean | 必須 | 追加制約なし | 登録後の編集有無 |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| expires_on | anyOf(string (date), null) | 必須 | 追加制約なし | 表示期限 |
| form_id | string (uuid) | 必須 | 追加制約なし | 食材形態 |
| id | string (uuid) | 必須 | 追加制約なし | 不変の行識別子 |
| location | string | 必須 | minLength=1; maxLength=20000 | 冷蔵・冷凍・常温の保管場所 |
| opened_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 開封時点 |
| original_amount | anyOf(string, null) | 必須 | anyOfの制約=string: pattern="^(?!^[-+.]*$)[+-]?0*(?:\\d{0,14}&#124;(?=[\\d.]{1,21}0*$)\\d{0,14}\\.\\d{0,6}0*$)" | 登録時数量。不明はNULL |
| original_form_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 登録時の食材形態 |
| original_unit_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 登録時単位 |
| priority | string | 必須 | minLength=1; maxLength=20000 | 先に使う優先指定 |
| product_version_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 商品版 |
| quantity_quality | string | 必須 | minLength=1; maxLength=20000 | 数量の確定・不明 |
| source_import_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 登録元レシート |
| status | string | 必須 | minLength=1; maxLength=20000 | 在庫の有効・削除・レシート取消状態 |
| unit_id | string (uuid) | 必須 | 追加制約なし | 単位 |
| updated_at | string (date-time) | 必須 | 追加制約なし | 最終編集日時 |
| user_id | string (uuid) | 必須 | 追加制約なし | 所有者 |

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
"""手持ち食材ロットの削除。具体例は専用型と操作別受入テストに対応する。"""

OPERATION_ID = "entity_pantry_lot_delete"
TABLE = "pantry_lot"
ACTION = "delete"
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "手持ち食材ロットの削除。認証情報は依存から取得し、本人所有または管理者権限を検査する。",
  "operationId": "entity_pantry_lot_delete",
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
  "responses": {
    "200": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/PantryLotRow"
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
  "summary": "手持ち食材ロットの削除",
  "tags": [
    "正規化データ: 手持ち食材ロット"
  ]
}
```
