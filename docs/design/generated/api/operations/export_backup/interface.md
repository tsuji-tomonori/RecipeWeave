# インターフェース: export_backup

[詳細](detail.md) / [入出力](interface.md) / [ログ](messages.md) / [SQL](queries.md) / [シーケンス](sequence.md) / [要因別試験](tests.md) / [API一覧](../../README.md)

実装から自動生成。手編集禁止。`uv run python tools/generate_service_design.py` で更新。

`POST /api/backups/export` — バックアップを書き出す

## 認証

[{"HTTPBearer": []}]

宣言: 検証済みBearerトークンと本人所有権

## パラメーター

なし。

## リクエスト本文

リクエスト本文の定義なし。

## レスポンス

### HTTP 200: Successful Response

Content-Type: `application/json`

BackupDocument-Output

| 項目 | 型 | 必須性 | 制約 | 説明 |
|---|---|---|---|---|
| artifactId | string (uuid) | 必須 | 追加制約なし | Artifactid |
| exportedAt | string (date-time) | 必須 | 追加制約なし | Exportedat |
| format | string | 必須 | const="recipeweave-relational" | Format |
| formatVersion | integer | 必須 | const=2 | Formatversion |
| ownerId | string (uuid) | 必須 | 追加制約なし | Ownerid |
| profile | BackupProfile | 必須 | 追加制約なし |  |
| sourceVersion | integer | 必須 | minimum=0.0 | Sourceversion |
| tables | BackupTables-Output | 必須 | 追加制約なし |  |

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
"""バックアップを書き出す。本人・版・確認の具体例はバックアップ受入試験に対応する。"""
```

[Swagger互換のOpenAPI JSON](interface.openapi.json)

[共有モデルの全仕様](../../MODELS.md) / [共通エラー](../../ERRORS.md)

## このAPIのOpenAPI定義

```json
{
  "description": "本人の現在データを書き出し、発行した本文の根拠だけを記録する。",
  "operationId": "export_backup",
  "parameters": [],
  "responses": {
    "200": {
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/BackupDocument-Output"
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
  "summary": "バックアップを書き出す",
  "tags": [
    "バックアップ"
  ]
}
```
