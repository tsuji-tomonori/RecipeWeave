# インターフェース: claim_shard

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/generation/shards/claim` — 生成範囲のリース取得

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
| lease_seconds | integer | 任意 | default=120; minimum=30.0; maximum=3600.0 | Lease Seconds |
| template_id | anyOf(string (uuid), null) | 任意 | 追加制約なし | Template Id |

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
"""生成範囲のリース取得の例。フェンスは取得結果を使う。"""

SAMPLE = {"lease_seconds": 120}
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "operationId": "claim_shard",
  "parameters": [],
  "requestBody": {
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/app__apis__generation__claim_shard__schemas__Request"
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
  "summary": "生成範囲のリース取得",
  "tags": [
    "生成運用"
  ]
}
```
