# インターフェース: entity_backup_restore_intent_get

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`GET /api/entities/backup_restore_intent/{row_id}` — 復元内容の確認記録。本人・本文・確認時の更新版・期限を固定し、一度だけ消費するの取得

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

BackupRestoreIntentRow

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| artifact_id | string (uuid) | 必須 | 追加制約なし | 本人へ発行したバックアップ証拠の識別子 |
| body_sha256 | string | 必須 | minLength=1; maxLength=20000 | 確認した本文全体のSHA-256。発行記録と一致する |
| consumed_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 復元と同一トランザクションで確定する使用日時。取消・再使用は不可 |
| created_at | string (date-time) | 必須 | 追加制約なし | 復元内容を検証して確認記録を発行した日時(UTC) |
| current_revision | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 確認時の現在データの更新版。復元直前にも同じ値であることを検査する |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| expires_at | string (date-time) | 必須 | 追加制約なし | 確認の有効期限。発行から最大15分 |
| id | string (uuid) | 必須 | 追加制約なし | 確認画面へ返す不変の復元確認識別子 |
| user_id | anyOf(string (uuid), null) | 必須 | 追加制約なし | 復元する本人。利用者消去後だけNULLへ匿名化する |

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
"""復元内容の確認記録。本人・本文・確認時の更新版・期限を固定し、一度だけ消費するの取得。具体例は専用型と操作別受入テストに対応する。"""

OPERATION_ID = "entity_backup_restore_intent_get"
TABLE = "backup_restore_intent"
ACTION = "get"
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "復元内容の確認記録。本人・本文・確認時の更新版・期限を固定し、一度だけ消費するの取得。認証情報は依存から取得し、本人所有または管理者権限を検査する。",
  "operationId": "entity_backup_restore_intent_get",
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
            "$ref": "#/components/schemas/BackupRestoreIntentRow"
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
  "summary": "復元内容の確認記録。本人・本文・確認時の更新版・期限を固定し、一度だけ消費するの取得",
  "tags": [
    "正規化データ: 復元内容の確認記録。本人・本文・確認時の更新版・期限を固定し、一度だけ消費する"
  ]
}
```
