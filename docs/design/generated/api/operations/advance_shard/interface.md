# インターフェース: advance_shard

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`PUT /api/generation/shards/{row_id}/progress` — 生成範囲の進捗確定

## 認証

[{"HTTPBearer": []}]

宣言: bearer

## パラメーター

| 場所 | 名前 | 必須性 | 型 | 制約 | 説明 |
|---|---|---|---|---|---|
| path | row_id | 必須 | string (uuid) | 追加制約なし |  |

## リクエスト本文

必須

### application/json

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| expected_fence | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | Expected Fence |
| next_ordinal | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | Next Ordinal |
| state | string | 必須 | enum=["running", "done"] | State |

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

GenerationShardRow

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| created_at | string (date-time) | 必須 | 追加制約なし | 作成日時 |
| end_ordinal | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 終了序数(排他的) |
| etag | string | 必須 | pattern="^[0-9]+$" | 更新・削除時のIf-Matchに使う行版 |
| fence_token | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 古い所有者の書込みを拒否 |
| id | string (uuid) | 必須 | 追加制約なし | 不変ID |
| lease_expires_at | anyOf(string (date-time), null) | 必須 | 追加制約なし | 有効期限 |
| lease_owner | anyOf(string, null) | 必須 | anyOfの制約=string: minLength=1; maxLength=20000 | ワーカー識別子 |
| next_ordinal | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 再開位置 |
| start_ordinal | string | 必須 | pattern="^-?(0&#124;[1-9][0-9]{0,18})$" | 開始序数 |
| state | string | 必須 | enum=["queued", "running", "done", "failed"] | 待機/実行/完了/停止 |
| template_id | string (uuid) | 必須 | 追加制約なし | テンプレート版 |

### HTTP 401: 認証必須

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 403: 運用権限なし

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 409: リース競合・対象なし

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 422: 入力不正

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 503: DB接続不可

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

## 操作のサンプル

```python
"""生成範囲の進捗確定の例。フェンスは取得結果を使う。"""

SAMPLE = {"lease_seconds": 120}
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "operationId": "advance_shard",
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
  "requestBody": {
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/app__apis__generation__advance_shard__schemas__Request"
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
            "$ref": "#/components/schemas/GenerationShardRow"
          }
        }
      },
      "description": "Successful Response"
    },
    "401": {
      "description": "認証必須"
    },
    "403": {
      "description": "運用権限なし"
    },
    "409": {
      "description": "リース競合・対象なし"
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
  "summary": "生成範囲の進捗確定",
  "tags": [
    "生成運用"
  ]
}
```
