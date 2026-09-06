# インターフェース: preview_backup

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/backups/preview` — バックアップの全置換内容を検証する

## 認証

[{"HTTPBearer": []}]

宣言: 検証済みBearerトークンと本人所有権

## パラメーター

なし。

## リクエスト本文

必須

### application/json

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| backup | BackupDocument-Input | 必須 | 追加制約なし |  |

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

BackupPreview

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| backupSha256 | string | 必須 | pattern="^[0-9a-f]{64}$" | Backupsha256 |
| counts | array&lt;BackupCount&gt; | 必須 | 追加制約なし | Counts |
| expectedVersion | integer | 必須 | minimum=0.0 | Expectedversion |
| expiresAt | string (date-time) | 必須 | 追加制約なし | Expiresat |
| intentId | string (uuid) | 必須 | 追加制約なし | Intentid |
| preservedTargets | array&lt;string&gt; | 必須 | 追加制約なし | Preservedtargets |
| replaceTargets | array&lt;string&gt; | 必須 | 追加制約なし | Replacetargets |
| sourceVersion | integer | 必須 | minimum=0.0 | Sourceversion |

### HTTP 401: 本人・形式・版・確認・DB制約の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 403: 本人・形式・版・確認・DB制約の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 409: 本人・形式・版・確認・DB制約の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 413: 本人・形式・版・確認・DB制約の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 422: 本人・形式・版・確認・DB制約の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

### HTTP 503: 本人・形式・版・確認・DB制約の検証失敗

OpenAPIに本文schemaなし。共通エラー実装の定義はエラー仕様を参照。

## 操作のサンプル

```python
"""バックアップの全置換内容を検証する。本人・版・確認の具体例はバックアップ受入試験に対応する。"""
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "バックアップの全置換内容を検証する。利用者の確認がない全置換を受け付けない。",
  "operationId": "preview_backup",
  "parameters": [],
  "requestBody": {
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/BackupPreviewRequest"
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
            "$ref": "#/components/schemas/BackupPreview"
          }
        }
      },
      "description": "Successful Response"
    },
    "401": {
      "description": "本人・形式・版・確認・DB制約の検証失敗"
    },
    "403": {
      "description": "本人・形式・版・確認・DB制約の検証失敗"
    },
    "409": {
      "description": "本人・形式・版・確認・DB制約の検証失敗"
    },
    "413": {
      "description": "本人・形式・版・確認・DB制約の検証失敗"
    },
    "422": {
      "description": "本人・形式・版・確認・DB制約の検証失敗"
    },
    "503": {
      "description": "本人・形式・版・確認・DB制約の検証失敗"
    }
  },
  "security": [
    {
      "HTTPBearer": []
    }
  ],
  "summary": "バックアップの全置換内容を検証する",
  "tags": [
    "バックアップ"
  ]
}
```
